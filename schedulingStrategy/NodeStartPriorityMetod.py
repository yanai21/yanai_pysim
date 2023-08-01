from basicFunction.basicFunction import JobPlacement

from basicFunction.basicUrgentFunction.preemptionAlgorithm import PreemptionAlgorithm, DP

# from environment.class.system import nodeStartTime, writeBandwidth, idleEnergy_W, NUM_NODES, NUM_SLEEP_NODES
from basicFunction.basicUrgentFunction.nodeStartAlgorithm import NodeStart
from basicFunction.basicUrgentFunction.urgentJobPlacement import UrgentReserve

# from model import PreemptionOverhead
from basicFunction.countNode import countNode


# 緊急ジョブの割り当て
def NodeStartUrgentJobAssignment(Nodes, now, urgentJob, event, normalJob_queue, system):
    # ノードの確認
    empty_node = countNode(Nodes, 0)
    available_num_node = len(empty_node)
    use_nodes = urgentJob.nodes
    # Idleノードに割り当て
    if available_num_node >= use_nodes:
        JobPlacement(now, empty_node, urgentJob, event, Nodes, popNum=0)
    # Idleノードに割り当てられない時
    else:
        # 中断とノード起動のノード数を管理
        NUM_NODES_Preemption = 0
        NUM_NODES_NodeStart = 0
        # 中断もしくは起動に要する時間
        overheadTime = 0
        # 中断に要するテーブルの作成
        # Nodesから投入されているジョブリストを作成
        jobList = []
        for job in normalJob_queue:
            if job.status == 1:
                jobList.append(job)
        # 実行中のノード数をカウントする
        NUM_NODES = len(countNode(Nodes, 1))
        # 寝ているノード数をカウントする
        SLEEP_NODES_list = countNode(Nodes, -1)
        NUM_SLEEP_NODES = len(SLEEP_NODES_list)
        dp, breakdp = DP(len(jobList), NUM_NODES, jobList)
        # 必要なノード数の把握
        NUM_NEED_NODES = use_nodes - available_num_node
        # アルゴリズム
        if NUM_NEED_NODES <= NUM_SLEEP_NODES:
            NUM_NODES_NodeStart = NUM_NEED_NODES
            overheadTime = system.nodeStartTime_s
        else:
            NUM_NODES_NodeStart = NUM_SLEEP_NODES
            for i in range(NUM_NEED_NODES - NUM_SLEEP_NODES, NUM_NODES - NUM_SLEEP_NODES + 1):
                if dp[-1][i] != 0:
                    NUM_NODES_Preemption = i
                    NUM_NODES_NodeStart = NUM_NEED_NODES - i
                    overheadTime = max(
                        system.nodeStartTime_s, system.PreemptionOverhead(dp[-1][i], system.writeBandwidth_mb)
                    )
                    break
        # アルゴリズム終了
        NUM_NODES_Idle = use_nodes - (NUM_NODES_NodeStart + NUM_NODES_Preemption)
        print("PreemptionNodes:{}".format(NUM_NODES_Preemption))
        print("NodeStartNodes:{}".format(NUM_NODES_NodeStart))
        print("idleNode:{}".format(NUM_NODES_Idle))
        # 緊急ジョブを割り当てるノードを決定
        finishtime = now + overheadTime
        # urgentJobのstatusの変更
        urgentJob.status = 0
        # # Preemption
        # if NUM_NODES_Preemption != 0:
        #     urgentJob.preemptionJobs = breakdp[-1][NUM_NODES_Preemption]
        #     PreemptionAlgorithm(urgentJob, Nodes, now, event, preemptionJobs, preemptionNodes, result, reservedNodes)
        # NodeStart
        if NUM_NODES_NodeStart != 0:
            # 起動するノードリストを作成
            for i in range(NUM_NODES_NodeStart):
                urgentJob.startNodes.append(SLEEP_NODES_list[i])
            NodeStart(urgentJob, Nodes, event, now, system)
        # idleNode
        if NUM_NODES_Idle != 0:
            for i in range(use_nodes):
                assigned_node = empty_node.pop(0)
                if assigned_node.status == 0:
                    assigned_node.status = 2
                    urgentJob.runNode.append(assigned_node)
                else:
                    print("緊急ジョブを空きノードから割り当てたが失敗")
                    exit()
        # 緊急ジョブの割り当て時刻をeventに追加
        try:
            urgentJob.event[finishtime].append("urgentJobStart")
        except:
            urgentJob.event[finishtime] = ["urgentJobStart"]
        # UrgentReserve(urgentJob, Nodes, event, finishtime, now)
