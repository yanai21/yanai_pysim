import os
import copy
from environment.global_var import *
from log.log import LogNormalJob, LogNodes, LogResult, VisualizationJob, VisualizationNode, NodeResult
from basicFunction.normalJobAssignment import NormalJobAssignment
from basicFunction.basicFunction import FinishJob
from nodeClass import Node
from basicFunction.basicUrgentFunction.preemptionAlgorithm import (
    PreemptionFinish,
    PreemptionRecover,
    PreemptionRecoverFinish,
)
from basicFunction.basicUrgentFunction.nodeStartAlgorithm import NodeStartFinish
from basicFunction.basicUrgentFunction.urgentJobPlacement import UrgentJobPlacement
from basicFunction.basicUrgentFunction.urgentJobAssignment import UrgentJobAssignment
from evaluation.evaluation import ElectricPower, Makespan, EnergyConsumption, deadlineRatio


# スケジューリング
def scheduling(name, UrgentFlag, UrgentJobStrategy, environment):
    # print(environment.system.sleepNodes)
    # 前回のログを消すために必要
    try:
        os.remove("./log/{}/Nodes.txt".format(name))
    except:
        pass
    global Nodes, now, event, result
    # ノード関係
    systemNodes = environment.system.systemNodes
    Nodes = [Node(id, 0) for id in range(systemNodes)]
    for id in range(environment.system.sleepNodes):
        Nodes[id].status = -1
    # 結果用
    electricPowerResult = []
    result = []
    nodeResult = {}
    # 現時刻
    now = 0
    normalJob_queue = copy.deepcopy(environment.normalJob_queue)
    event = copy.deepcopy(environment.event)
    if UrgentFlag:
        urgentJob_queue = copy.deepcopy(environment.urgentJob_queue)
    else:
        urgentJob_queue = []
        for key in list(event):
            event_tmp = event[key]
            for value in event[key]:
                if value.type == "urgent":
                    event_tmp.remove(value)
            if len(event_tmp) != 0:
                event[key] = event_tmp
            else:
                event.pop(key)
    # 結果確認
    # print("normalJob_queue:{}".format(normalJob_queue))
    # print("urgentJob:{}".format(urgentJob_queue))
    # print("event:{}".format(event))

    # 1回目
    NormalJobAssignment(now, event, Nodes, normalJob_queue)
    LogNodes(name, now, Nodes)
    # eventの並び替え
    event = sorted(event.items())
    event = dict((x, y) for x, y in event)

    # ２回目以降
    while len(event) != 0:
        # eventの並び替え
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        # 終了ジョブをNodesから取り除く
        now = next(iter(event))
        eventJobs = event.pop(now)
        # 電力を計算
        electricPowerResult = ElectricPower(electricPowerResult, now, Nodes, environment.system)
        # ノード状況を保存
        nodeResult = NodeResult(now, Nodes, nodeResult)
        for eventJob in reversed(eventJobs):
            # ノードのシャットダウン
            if eventJob.type == "node":
                # ノードシャットダウン開始
                if eventJob.status == 0:
                    eventJob.nodeShutdown(event, environment.system, now)
                # ノードシャットダウン終了
                elif eventJob.status == -22:
                    eventJob.nodeShutdownFinish()
            # 割り当て前の緊急ジョブ
            elif eventJob.type == "urgent" and eventJob.status == -1:
                UrgentJobAssignment(
                    Nodes, now, eventJob, event, normalJob_queue, environment.system, UrgentJobStrategy, result
                )
            # 実行前の緊急ジョブ
            elif eventJob.type == "urgent" and eventJob.status == 0:
                for urgent_event in eventJob.event[now]:
                    if urgent_event == "NodeStartFinish":
                        NodeStartFinish(eventJob)
                    elif urgent_event == "urgentJobStart":
                        UrgentJobPlacement(now, eventJob, event, environment.system)
                    elif urgent_event == "preemptionFinish":
                        PreemptionFinish(eventJob)
                    else:
                        print("変なイベントが緊急ジョブに投入されている")
            # 実行終了後の緊急ジョブ
            elif eventJob.type == "urgent" and eventJob.status == 1:
                FinishJob(now, eventJob, Nodes, result, event, environment.system)
                # 中断を使ったかどうか
                if len(eventJob.preemptionJobs) != 0:
                    PreemptionRecover(eventJob, event, now, environment.system)
            elif eventJob.type == "urgent" and eventJob.status == 2:
                for urgent_event in eventJob.event[now]:
                    if urgent_event == "preemptionRecoverFinish":
                        PreemptionRecoverFinish(eventJob, now, event)
                    else:
                        print("変なイベントが緊急ジョブに投入されている")
            elif eventJob.type == "normal" and eventJob.status == -1:
                normalJob_queue.append(eventJob)
            else:
                FinishJob(now, eventJob, Nodes, result, event, environment.system)
        NormalJobAssignment(now, event, Nodes, normalJob_queue)
        LogNodes(name, now, Nodes)
    energyConsumption = EnergyConsumption(electricPowerResult)
    # for tmp in result:
    #     if tmp[0] < 0:
    #         print(tmp)
    # # print(result)
    LogResult(name, result)
    makespan = Makespan(result)
    if UrgentFlag == True:
        deadlineratio = deadlineRatio(urgentJob_queue)
    else:
        deadlineratio = 0
    # # 単位時刻あたりのジョブ状況
    # VisualizationJob(result)
    # 単位時刻あたりのノード状況
    VisualizationNode(nodeResult)
    return makespan, electricPowerResult, energyConsumption, deadlineratio
