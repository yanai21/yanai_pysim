from basicFunction.basicFunction import JobPlacement, FinishJob


def NodeStart(urgentJob, Nodes, event, now, system):
    for node in urgentJob.startNodes:
        if node.status == -1:
            finishtime = now + system.nodeStartTime_s
            node.status == -21
            urgentJob.runNode.append(node)
            try:
                urgentJob.event[finishtime].append("NodeStartFinish")
                event[finishtime].append(urgentJob)
            except:
                urgentJob.event[finishtime] = ["NodeStartFinish"]
                event[finishtime] = [urgentJob]
            # for idx in range(NUM_NODES, NUM_NODES + NUM_Start_NODES):
            #     Nodes.append(["nodeStart"])
            #     startNodes.append(idx)
            # reservedNodes.extend(startNodes)
        else:
            print("ノード起動できません")
            exit()


def NodeStartFinish(Nodes, reservedNodes, startNodes):
    for idx in startNodes:
        Nodes[idx] = ["reserved"]


def NodeShutdown(now, Nodes, empty_node, startNodes, event):
    # 立ち上がったNodeをシャットダウン
    for idx in reversed(startNodes):
        empty_node.remove(idx)
        Nodes[idx] = ["shutdown"]
    # イベントに追加
    finishTime = now + nodeEndTime
    try:
        event[finishTime].append("shutdown")
    except:
        event[finishTime] = ["shutdown"]


def NodeShutdownFinish(startNodes, Nodes):
    for idx in reversed(startNodes):
        Nodes.pop(idx)
    startNodes = []
    return startNodes
