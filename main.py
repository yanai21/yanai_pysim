from evaluation import Makespan,EnergyConsumption
from basicFunction import JobPlacement,FinishJob,NormalJobPlacement
from basicUrgentFunction.preemptionAlgorithm import PreemptionAlgorithm,PreemptionRecover,DP
from system import nodeStartTime,writeBandwidth,idleEnergy_W,NUM_NODES,NUM_SLEEP_NODES
from basicUrgentFunction.nodeStartAlgorithm import NodeShutdown,NodeShutdownFinish,NodeStartFinish
from basicUrgentFunction.killAlgorithm import KillAlgorithm
from basicUrgentFunction.urgentJobPlacement import UrgentJobPlacement
from model import PreemptionOverhead
from schedulingStrategy.ProposedMethod import ProposedUrgentJobAssignment
from schedulingStrategy.PreemptionPriorityMethod import PreemptionUrgentJobAssignment
from schedulingStrategy.NodeStartPriorityMetod import NodeStartUrgentJobAssignment
import job.jobSet as jobSet 
import copy
from gragh import MakeSpanGragh,EnergyConsumptionGragh

from global_var import *

#スケジューリング
def main(UrgentFlag,UrgentJobAssignment):
    global Nodes,empty_node,preemptionJobs,startNodes,reservedNodes,now,normalJob_queue,urgentJob_queue,event,result
    #ノード関係
    Nodes = [[] for _ in range(NUM_NODES)]
    empty_node = [i for i in range(NUM_NODES)]
    #緊急ジョブ関係
    preemptionJobs=[]
    startNodes=[]
    reservedNodes = []
    #現時刻
    now = 0
    normalJob_queue = copy.deepcopy(jobSet.normalJob_queue)
    if(UrgentFlag):
        urgentJob_queue = copy.deepcopy(jobSet.urgentJob_queue)
        event = copy.deepcopy(jobSet.event)
    else:
        event ={}
    #結果用
    result=[]
    #通常ジョブ割り当て
    def NormalJobAssignment(event,Nodes,empty_node,normalJob_queue):
        remove_idx = []
        for idx, job in enumerate(normalJob_queue):
            use_nodes = job.nodes

            #ノードが空いているかの確認
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break
            #空いてるノードに配置
            if available_num_node >= use_nodes:
                JobPlacement(now,use_nodes,empty_node,job,event,Nodes,popNum=0)
                remove_idx.append(idx)
        #ジョブキューから配置したジョブを削除
        for idx in reversed(remove_idx):
            normalJob_queue.pop(idx)
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)

    #1回目
    NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
    print(now)
    print(Nodes)
    #２回目以降
    while len(event) != 0:
        #終了ジョブをNodesから取り除く
        now=next(iter(event))
        eventJobs=event.pop(now)
        for eventJob in eventJobs:
            #中断とノードスタートの通知
            if(eventJob == "nodeStart"):
                #Nodesを書き換え
                NodeStartFinish(Nodes,reservedNodes,startNodes)
            elif(eventJob == "shutdown"):
                NodeShutdownFinish(startNodes,Nodes)
            #割り当て前の緊急ジョブ
            elif(eventJob.type=="urgent" and eventJob.status == ""):
                empty_node = sorted(empty_node)
                UrgentJobAssignment(Nodes,empty_node,preemptionJobs,startNodes,reservedNodes,now,eventJob,event,result)
            #予約された緊急ジョブ
            elif(eventJob.type=="urgent" and eventJob.status == "reserved"):
                UrgentJobPlacement(now,eventJob,Nodes,event,reservedNodes)
            #実行終了した緊急ジョブ
            elif(eventJob.type=="urgent" and eventJob.status == "run"):
                FinishJob(now,eventJob,Nodes,empty_node,result)
                for method in eventJob.method:
                    if(method == "nodestart"):
                        NodeShutdown(now,Nodes,empty_node,startNodes,event)
            else:
                #通常ジョブの終了
                FinishJob(now,eventJob,Nodes,empty_node,result)   
        empty_node = sorted(empty_node)
        NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
        print(now)
        print(Nodes)
        print(event)
    print(result)

if __name__ == "__main__":
    # print("提案手法")
    # proposedMakespan,proposedEnergyConsumption= main(True,ProposedUrgentJobAssignment)
    # print("中断優先")
    # preemptionMakespan,preemptionEnergyConsumption = main(True,PreemptionUrgentJobAssignment)
    print("ノード起動優先")
    main(True,NodeStartUrgentJobAssignment)
    # print("通常ジョブのみ")
    # main(False,NormalJobPlacement)