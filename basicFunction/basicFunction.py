# 配置関数 (Nodesの追加、empty_nodeから取り出す、eventに追加)
def JobPlacement(now, empty_node, job, event, Nodes, popNum):
    etime = job.etime
    job.status = 1
    finish_time = now + etime
    use_nodes = job.nodes
    for i in range(use_nodes):
        assigned_node = empty_node.pop(popNum)
        if assigned_node.status == 0:
            assigned_node.status = 1
            job.runNode.append(assigned_node)
        else:
            print("通常ジョブの割り当てに失敗")
            exit()
        # start時刻の書き込み
        job.startTime = now

    try:
        event[finish_time].append(job)
    except:
        event[finish_time] = [job]


# 終了したジョブ動作
def FinishJob(now, eventJob, Nodes, result):
    if eventJob.status == 1:
        # 終了時刻記入
        eventJob.endTime = now
        eventJob.status = 2
        runNodes = []
        for node in eventJob.runNode:
            runNodes.append(node.id)
        # 結果書き込み
        result.append([eventJob.id, eventJob.startTime, eventJob.endTime, runNodes, eventJob.status])
        # Nodesから取り除く
        for node in eventJob.runNode:
            node.status = 0
    else:
        print(eventJob.status)
        print("終了できないジョブです")
        exit()


# 通常ジョブのみで実行する際の引数用
def NormalJobPlacement():
    return
