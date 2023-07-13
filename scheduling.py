from evaluation.evaluation import Makespan,ElectricPower
from basicFunction.basicFunction import JobPlacement,FinishJob,NormalJobPlacement
from basicUrgentFunction.preemptionAlgorithm import PreemptionFinish,PreemptionRecover,PreemptionRecoverFinish
from environment.class.system import nodeStartTime,writeBandwidth,idleEnergy_W,NUM_NODES,NUM_SLEEP_NODES
from basicUrgentFunction.nodeStartAlgorithm import NodeShutdown,NodeShutdownFinish,NodeStartFinish
from basicUrgentFunction.urgentJobPlacement import UrgentJobPlacement
from schedulingStrategy.ProposedMethod import ProposedUrgentJobAssignment
from schedulingStrategy.PreemptionPriorityMethod import PreemptionUrgentJobAssignment
from schedulingStrategy.NodeStartPriorityMetod import NodeStartUrgentJobAssignment
import job.jobSet as jobSet 
from log import LogNormalJob,LogResult,LogNodes
import copy
from evaluation.gragh import MakeSpanGragh,ElectricPowerGragh
import os
from global_var import *

#スケジューリング
def scheduling(name,UrgentFlag,UrgentJobAssignment):
    #前回のログを消すために必要
    try:
        os.remove('./log/{}/Nodes.txt'.format(name))
    except:
        pass
    global Nodes,empty_node,now,normalJob_queue,urgentJob_queue,event,result
    #ノード関係
    Nodes = [[] for _ in range(NUM_NODES)]
    empty_node = [i for i in range(NUM_NODES)]
    #緊急ジョブ関係
    preemptionJobs=[]
    preemptionNodes =[]
    startNodes=[]
    reservedNodes = []
    electricPowerResult = []
    #現時刻
    now = 0
    normalJob_queue = copy.deepcopy(jobSet.normalJob_queue)
    if(UrgentFlag):
        urgentJob_queue = copy.deepcopy(jobSet.urgentJob_queue)
        event = copy.deepcopy(jobSet.event)
    else:
        urgentJob_queue = []
        event ={}
    LogNormalJob(name,normalJob_queue,urgentJob_queue)
    #結果用
    result=[]

    #1回目
    NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
    LogNodes(name,now,Nodes)
    #eventの並び替え
    event = sorted(event.items())
    event = dict((x, y) for x, y in event)
    # print("now:{}".format(now))
    # print(Nodes)
    #２回目以降
    while len(event) != 0:
        #eventの並び替え
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        #終了ジョブをNodesから取り除く
        now=next(iter(event))
        eventJobs=event.pop(now)
        for eventJob in reversed(eventJobs):
            #TODO:この分岐が多すぎる…
            #起動によってできるイベント
            if(eventJob == "nodeStart"):
                #Nodesを書き換え
                NodeStartFinish(Nodes,reservedNodes,startNodes)
            elif(eventJob == "shutdown"):
                startNodes=NodeShutdownFinish(startNodes,Nodes)
            #中断によってできるイベント
            elif(eventJob == "preemption"):
                PreemptionFinish(Nodes,preemptionNodes)
            elif(eventJob == "recover"):
                preemptionJobs,event = PreemptionRecoverFinish(Nodes,now,preemptionJobs,event)
            elif(eventJob ==""):
                pass
            #割り当て前の緊急ジョブ
            elif(eventJob.type=="urgent" and eventJob.status == ""):
                empty_node = sorted(empty_node)
                preemptionJobs,startNodes,reservedNodes,preemptionNodes = UrgentJobAssignment(Nodes,empty_node,preemptionJobs,startNodes,reservedNodes,preemptionNodes,now,eventJob,event,result)
            #予約された緊急ジョブ
            elif(eventJob.type=="urgent" and eventJob.status == "reserved"):
                reservedNodes = UrgentJobPlacement(now,eventJob,Nodes,event,reservedNodes)
            #実行終了した緊急ジョブ
            elif(eventJob.type=="urgent" and eventJob.status == "run"):
                FinishJob(now,eventJob,Nodes,empty_node,result)
                for method in eventJob.method:
                    if(method == "nodestart"):
                        NodeShutdown(now,Nodes,empty_node,startNodes,event)
                    elif(method == "preemption"):
                        PreemptionRecover(eventJob,Nodes,now,preemptionNodes,event,empty_node)
            else:
                #通常ジョブの終了
                FinishJob(now,eventJob,Nodes,empty_node,result)   
        empty_node = sorted(empty_node)
        NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
        LogNodes(name,now,Nodes)
        # print("now:{}".format(now))
        # print(Nodes)
        #最大電力を計算
        electricPowerResult = ElectricPower(electricPowerResult,now,Nodes)
    for tmp in result:
        if(tmp[0]<0):
            print(tmp)
    # print(result)
    LogResult(name,result)
    makespan = Makespan(result)
    return makespan,electricPowerResult