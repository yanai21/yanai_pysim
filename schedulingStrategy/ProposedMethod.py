# 緊急ジョブの割り当て
def ProposedAlgorithm(urgentJob, available_num_node, NUM_SLEEP_NODES, NUM_NODES, dp, system, breakdp, jobList):
    # 中断とノード起動のノード数を管理
    NUM_NODES_Preemption = 0
    NUM_NODES_NodeStart = 0
    # 中断もしくは起動に要する時間
    overheadTime = 0
    use_nodes = urgentJob.nodes
    NUM_NEED_NODES = use_nodes - available_num_node
    # 緊急ジョブの締切時間の確認
    deadline = urgentJob.deadlineTime - (urgentJob.etime + urgentJob.occurrenceTime)
    if system.nodeStartTime_s <= deadline:
        if NUM_SLEEP_NODES < NUM_NEED_NODES:
            NUM_NODES_NodeStart = NUM_SLEEP_NODES
            # 足りない時はその分を中断で補う
            for i in range(NUM_NEED_NODES - NUM_SLEEP_NODES, NUM_NODES - NUM_SLEEP_NODES + 1):
                if dp[-1][i] != 0:
                    NUM_NODES_Preemption = i
                    NUM_NODES_NodeStart = NUM_NEED_NODES - i
                    overheadTime = max(
                        system.nodeStartTime_s, system.preemptionOverhead(dp[-1][i], system.writeBandwidth_mb)
                    )
                    break
        else:
            NUM_NODES_NodeStart = NUM_NEED_NODES
            overheadTime = system.nodeStartTime_s
        NUM_NODES_Idle = use_nodes - (NUM_NODES_NodeStart + NUM_NODES_Preemption)
    else:
        for i in range(NUM_NEED_NODES, len(dp[-1])):
            if dp[-1][i] != 0:
                NUM_NODES_Preemption = i
                overheadTime = system.preemptionOverhead(dp[-1][i], system.writeBandwidth_mb)
                break
        NUM_NODES_Idle = use_nodes - (NUM_NODES_NodeStart + NUM_NODES_Preemption)
    if NUM_NODES_Preemption != 0:
        urgentJob.preemptionJobs = breakdp[-1][NUM_NODES_Preemption]
    # idleノードが負の数になる可能性がある (nodeStartも！)
    NUM_NODES_Idle = max(0, NUM_NODES_Idle)
    NUM_NODES_NodeStart = max(0, NUM_NODES_NodeStart)
    return NUM_NODES_Preemption, NUM_NODES_NodeStart, NUM_NODES_Idle, overheadTime
