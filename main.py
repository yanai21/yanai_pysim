from evaluation import Makespan,EnergyConsumption
from basicFunction import JobPlacement,FinishJob
from basicUrgentFunction.preemptionAlgorithm import PreemptionAlgorithm,PreemptionRecover,DP
from system import nodeStartTime,writeBandwidth,idleEnergy_W,NUM_NODES,NUM_SLEEP_NODES
from basicUrgentFunction.nodeStartAlgorithm import NodeStart,NodeShutdown
from basicUrgentFunction.killAlgorithm import KillAlgorithm
from model import PreemptionOverhead
from schedulingStrategy.ProposedMethod import ProposedUrgentJobAssignment,PreemptionPriorityMethod,NodeStartPriorityMethod

import job.jobSet as jobSet 

#スケジューリング
def main(UrgentJobAssignment):
    Nodes = [[] for _ in range(NUM_NODES)]
    normalJob_queue = jobSet.normalJob_queue
    preemptionJobs=[]
    startNodes=[]
    energyConsumption = 0
    normalJob_queue = jobSet.normalJob_queue
    urgentJob_queue = jobSet.urgentJob_queue
    event = jobSet.event
    now = 0
    empty_node = [i for i in range(NUM_NODES)]
    result=[]


    def NormalJobAssignment(event,Nodes,empty_node,job_queue):
        remove_idx = []
        for idx, job in enumerate(job_queue):
            use_nodes = job.nodes

            #ノードが空いているかの確認
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break
            #空いてるノードに配置
            if available_num_node >= use_nodes:
                empty_node,job,event,Nodes=JobPlacement(now,use_nodes,empty_node,job,event,Nodes,popNum=0)
                remove_idx.append(idx)
        #ジョブキューから配置したジョブを削除
        for idx in reversed(remove_idx):
            job_queue.pop(idx)
        
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)

        return event,Nodes,empty_node,job_queue
    #1回目
    event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
    #２回目以降
    while len(event) != 0:
        #終了ジョブをNodesから取り除く
        now=next(iter(event))
        eventJobs=event.pop(now)
        for eventJob in reversed(eventJobs):
            #TODO:eventJobの種類が２つある場合を想定する必要がある
            #緊急ジョブの投入かどうかを判断
            if(eventJob.type=="urgent" and eventJob.startTime==0):
                empty_node = sorted(empty_node)
                event,Nodes,empty_node,preemptionJobs,startNodes,normalJob_queue,result,energyConsumption=UrgentJobAssignment(now,event,Nodes,empty_node,eventJob,preemptionJobs,normalJob_queue,startNodes,result,energyConsumption)
            elif(eventJob.type=="urgent" and len(eventJob.status) != 0):
                #結果書き込み、Nodesから排除
                eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result) 
                for status in eventJob.status:
                    if(status == "preemption"):  
                        #復帰
                        eventJob,Nodes,empty_node,preemptionJobs,event = PreemptionRecover(eventJob,Nodes,empty_node,now,preemptionJobs,event)
                    elif(status == "nodestart"):
                        eventJob,Nodes,empty_node,result,startNodes,energyConsumption = NodeShutdown(now,eventJob,Nodes,empty_node,result,startNodes,energyConsumption) 
            else:
                #結果書き込み、Nodesから排除
                eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result)   
        empty_node = sorted(empty_node)
        event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
                    
    #結果の出力
    print(result)
    makespan = Makespan(result)
    EnergyConsumption(result,makespan,NUM_NODES,energyConsumption)


if __name__ == "__main__":
    #提案手法の実行
    main(ProposedUrgentJobAssignment)