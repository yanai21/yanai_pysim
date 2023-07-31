import os
import copy
from environment.global_var import *
from log.log import LogNormalJob, LogNodes, LogResult
from basicFunction.normalJobAssignment import NormalJobAssignment
from basicFunction.basicFunction import FinishJob
from nodeClass import Node


# スケジューリング
def scheduling(name, UrgentFlag, UrgentJobAssignment, environment):
    # 前回のログを消すために必要
    try:
        os.remove("./log/{}/Nodes.txt".format(name))
    except:
        pass
    global nodes, now, event, result
    # ノード関係
    systemNodes = environment.system.systemNodes
    Nodes = [Node(id, 0) for id in range(systemNodes)]
    for id in range(environment.system.sleepNodes):
        Nodes[id].status = -1
    # 結果用
    electricPowerResult = []
    result = []
    # 現時刻
    now = 0
    normalJob_queue = copy.deepcopy(environment.normalJob_queue)
    if UrgentFlag:
        urgentJob_queue = copy.deepcopy(environment.urgentJob_queue)
        event = copy.deepcopy(environment.event)
    else:
        urgentJob_queue = []
        event = {}
    # 結果確認
    # print("normalJob_queue:{}".format(normalJob_queue))
    # print("urgentJob:{}".format(urgentJob_queue))
    # print("event:{}".format(event))

    LogNormalJob(name, normalJob_queue, urgentJob_queue)

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
        for eventJob in reversed(eventJobs):
            # 割り当て前の緊急ジョブ
            if eventJob.type == "urgent" and eventJob.status == -1:
                UrgentJobAssignment(Nodes, now, eventJob, event,normalJob_queue,environment.system)
            else:
                FinishJob(now, eventJob, Nodes, result)
        NormalJobAssignment(now, event, Nodes, normalJob_queue)
        LogNodes(name, now, Nodes)
    #         # 起動によってできるイベント
    #         if eventJob == "nodeStart":
    #             # Nodesを書き換え
    #             NodeStartFinish(Nodes, reservedNodes, startNodes)
    #         elif eventJob == "shutdown":
    #             startNodes = NodeShutdownFinish(startNodes, Nodes)
    #         # 中断によってできるイベント
    #         elif eventJob == "preemption":
    #             PreemptionFinish(Nodes, preemptionNodes)
    #         elif eventJob == "recover":
    #             preemptionJobs, event = PreemptionRecoverFinish(Nodes, now, preemptionJobs, event)
    #         elif eventJob == "":
    #             pass
    #         # 割り当て前の緊急ジョブ
    #         elif eventJob.type == "urgent" and eventJob.status == "":
    #             empty_node = sorted(empty_node)
    #             preemptionJobs, startNodes, reservedNodes, preemptionNodes = UrgentJobAssignment(
    #                 Nodes,
    #                 empty_node,
    #                 preemptionJobs,
    #                 startNodes,
    #                 reservedNodes,
    #                 preemptionNodes,
    #                 now,
    #                 eventJob,
    #                 event,
    #                 result,
    #             )
    #         # 予約された緊急ジョブ
    #         elif eventJob.type == "urgent" and eventJob.status == "reserved":
    #             reservedNodes = UrgentJobPlacement(now, eventJob, Nodes, event, reservedNodes)
    #         # 実行終了した緊急ジョブ
    #         elif eventJob.type == "urgent" and eventJob.status == "run":
    #             FinishJob(now, eventJob, Nodes, empty_node, result)
    #             for method in eventJob.method:
    #                 if method == "nodestart":
    #                     NodeShutdown(now, Nodes, empty_node, startNodes, event)
    #                 elif method == "preemption":
    #                     PreemptionRecover(eventJob, Nodes, now, preemptionNodes, event, empty_node)
    #         else:
    #             # 通常ジョブの終了
    #             FinishJob(now, eventJob, Nodes, empty_node, result)
    #         # 通常ジョブの終了
    #         empty_node = FinishJob(now, eventJob, Nodes, empty_node, result)
    #     empty_node = sorted(empty_node)
    #     empty_node, normalJob_queue = NormalJobAssignment(now, event, Nodes, empty_node, normalJob_queue)
    #     LogNodes(name, now, Nodes)
    #         # TODO:この分岐が多すぎる…
    #         # 起動によってできるイベント
    #         if eventJob == "nodeStart":
    #             # Nodesを書き換え
    #             NodeStartFinish(Nodes, reservedNodes, startNodes)
    #         elif eventJob == "shutdown":
    #             startNodes = NodeShutdownFinish(startNodes, Nodes)
    #         # 中断によってできるイベント
    #         elif eventJob == "preemption":
    #             PreemptionFinish(Nodes, preemptionNodes)
    #         elif eventJob == "recover":
    #             preemptionJobs, event = PreemptionRecoverFinish(Nodes, now, preemptionJobs, event)
    #         elif eventJob == "":
    #             pass
    #         # 割り当て前の緊急ジョブ
    #         elif eventJob.type == "urgent" and eventJob.status == "":
    #             empty_node = sorted(empty_node)
    #             preemptionJobs, startNodes, reservedNodes, preemptionNodes = UrgentJobAssignment(
    #                 Nodes,
    #                 empty_node,
    #                 preemptionJobs,
    #                 startNodes,
    #                 reservedNodes,
    #                 preemptionNodes,
    #                 now,
    #                 eventJob,
    #                 event,
    #                 result,
    #             )
    #         # 予約された緊急ジョブ
    #         elif eventJob.type == "urgent" and eventJob.status == "reserved":
    #             reservedNodes = UrgentJobPlacement(now, eventJob, Nodes, event, reservedNodes)
    #         # 実行終了した緊急ジョブ
    #         elif eventJob.type == "urgent" and eventJob.status == "run":
    #             FinishJob(now, eventJob, Nodes, empty_node, result)
    #             for method in eventJob.method:
    #                 if method == "nodestart":
    #                     NodeShutdown(now, Nodes, empty_node, startNodes, event)
    #                 elif method == "preemption":
    #                     PreemptionRecover(eventJob, Nodes, now, preemptionNodes, event, empty_node)
    #         else:
    #             # 通常ジョブの終了
    #             FinishJob(now, eventJob, Nodes, empty_node, result)
    #     empty_node = sorted(empty_node)
    #     NormalJobAssignment(event, Nodes, empty_node, normalJob_queue)
    #     LogNodes(name, now, Nodes)
    #     # print("now:{}".format(now))
    #     # print(Nodes)
    #     # 最大電力を計算
    #     electricPowerResult = ElectricPower(electricPowerResult, now, Nodes)
    # for tmp in result:
    #     if tmp[0] < 0:
    #         print(tmp)
    # # print(result)
    LogResult(name, result)
    # makespan = Makespan(result)
    # return makespan, electricPowerResult
