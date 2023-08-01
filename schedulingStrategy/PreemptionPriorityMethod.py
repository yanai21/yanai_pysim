# 緊急ジョブの割り当て
def PreemptionPriorityAlgorithm(urgentJob, available_num_node, NUM_SLEEP_NODES, NUM_NODES, dp, system):
    # 中断とノード起動のノード数を管理
    NUM_NODES_Preemption = 0
    NUM_NODES_NodeStart = 0
    # 中断もしくは起動に要する時間
    overheadTime = 0
    use_nodes = urgentJob.nodes
    NUM_NEED_NODES = use_nodes - available_num_node
    for i in range(NUM_NEED_NODES, len(dp[-1])):
        if dp[-1][i] != 0:
            NUM_NODES_Preemption = i
            overheadTime = system.PreemptionOverhead(dp[-1][i], system.writeBandwidth_mb)
            break
    NUM_NODES_Idle = use_nodes - (NUM_NODES_NodeStart + NUM_NODES_Preemption)
    return NUM_NODES_Preemption, NUM_NODES_NodeStart, NUM_NODES_Idle, overheadTime
