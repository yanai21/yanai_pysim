# 緊急ジョブの割り当て
def NodeStartPriorityAlgorithm(urgentJob, available_num_node, NUM_SLEEP_NODES, NUM_NODES, dp, system, breakdp,jobList):
    # 中断とノード起動のノード数を管理
    NUM_NODES_Preemption = 0
    NUM_NODES_NodeStart = 0
    # 中断もしくは起動に要する時間
    overheadTime = 0
    use_nodes = urgentJob.nodes
    NUM_NEED_NODES = use_nodes - available_num_node
    # アルゴリズム
    if NUM_NEED_NODES <= NUM_SLEEP_NODES:
        NUM_NODES_NodeStart = NUM_NEED_NODES
        overheadTime = system.nodeStartTime_s
    else:
        print(NUM_SLEEP_NODES)
        NUM_NODES_NodeStart = NUM_SLEEP_NODES
        for i in range(NUM_NEED_NODES - NUM_SLEEP_NODES, NUM_NODES - NUM_SLEEP_NODES + 1):
            if dp[-1][i] != 0:
                NUM_NODES_Preemption = i
                NUM_NODES_NodeStart = NUM_NEED_NODES - i
                overheadTime = max(
                    system.nodeStartTime_s, system.preemptionOverhead(dp[-1][i], system.writeBandwidth_mb)
                )
                break
    NUM_NODES_Idle = use_nodes - (NUM_NODES_NodeStart + NUM_NODES_Preemption)
    if NUM_NODES_Preemption != 0:
        # TODO:ランダム手法かどうかはここで判断する必要がありそう
        urgentJob.preemptionJobs = breakdp[-1][NUM_NODES_Preemption]
    # idleノードが負の数になる可能性がある (nodeStartも！)
    NUM_NODES_Idle = max(0, NUM_NODES_Idle)
    NUM_NODES_NodeStart = max(0, NUM_NODES_NodeStart)
    return NUM_NODES_Preemption, NUM_NODES_NodeStart, NUM_NODES_Idle, overheadTime
