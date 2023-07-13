from system import nodeStartTime, idleEnergy_W, nodeEndTime
from basicFunction import JobPlacement, FinishJob


def NodeStart(NUM_Start_NODES, NUM_SLEEP_NODES, NUM_NODES, urgentJob, now, Nodes, event, startNodes, reservedNodes):
    if NUM_SLEEP_NODES >= NUM_Start_NODES:
        # node起動を用いたことを加える
        urgentJob.method.append("nodestart")
        # イベントに追加
        finishtime = now + nodeStartTime
        try:
            event[finishtime].afppend("nodeStart")
        except:
            event[finishtime] = ["nodeStart"]
        for idx in range(NUM_NODES, NUM_NODES + NUM_Start_NODES):
            Nodes.append(["nodeStart"])
            startNodes.append(idx)
        reservedNodes.extend(startNodes)
    else:
        print("ノード起動できません")
        exit()
    return startNodes, reservedNodes


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
