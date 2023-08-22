import random


def RandomPreemptionAlgorithm(urgentJob, available_num_node, NUM_SLEEP_NODES, NUM_NODES, dp, system, breakdp, jobList):
    # 中断とノード起動のノード数を管理
    NUM_NODES_Preemption = 0
    NUM_NODES_NodeStart = 0
    # 中断もしくは起動に要する時間
    overheadTime = 0
    totalmemory = 0
    use_nodes = urgentJob.nodes
    NUM_NEED_NODES = use_nodes - available_num_node
    # TODO:ランダムでジョブを選択
    Bool = True
    # 対象のデータリスト
    pop_list = [i for i in range(len(jobList))]
    while Bool:
        if NUM_NEED_NODES <= NUM_NODES_Preemption:
            Bool = False
        # jobListからとるデータを選ぶ
        dataListNum = len(pop_list) - 1
        n = random.randint(0, dataListNum)
        job = jobList[pop_list.pop(n)]
        urgentJob.preemptionJobs.append(job)
        NUM_NODES_Preemption += job.nodes
        totalmemory += job.memory
    overheadTime += system.preemptionOverhead(totalmemory, system.writeBandwidth_mb)
    NUM_NODES_Idle = use_nodes - (NUM_NODES_NodeStart + NUM_NODES_Preemption)
    # idleノードが負の数になる可能性がある
    NUM_NODES_Idle = max(0, NUM_NODES_Idle)
    return NUM_NODES_Preemption, NUM_NODES_NodeStart, NUM_NODES_Idle, overheadTime
