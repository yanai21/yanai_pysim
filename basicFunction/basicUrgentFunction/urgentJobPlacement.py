def UrgentJobPlacement(now,urgentJob,Nodes,event,reservedNodes):
    etime = urgentJob.etime
    finish_time = now + etime
    urgentJob.startTime=now
    urgentJob.eEndTime=finish_time
    urgentJob.status = "run"
    for idx in reservedNodes:
        Nodes[idx] = [urgentJob]
    try:
        event[finish_time].append(urgentJob)
    except:
        event[finish_time] = [urgentJob]
    reservedNodes = []
    return reservedNodes

def UrgentReserve(urgentJob, empty_node, Nodes, event, reservedNodes, finishtime):
    # urgentNodesのStatusの変更
    etime = urgentJob.etime
    use_nodes = urgentJob.nodes
    urgentJob.status = "reserved"
    print(len(reservedNodes))
    if use_nodes > len(reservedNodes):
        for _ in range(use_nodes - len(reservedNodes)):
            idx = empty_node.pop(0)
            reservedNodes.append(idx)
    for arrange_node_idx in reservedNodes:
        if Nodes[arrange_node_idx] == []:
            Nodes[arrange_node_idx] = ["reserved"]
        # 予約ノードを書き込み
        urgentJob.runNode.append(arrange_node_idx)
    # eventの追加
    try:
        tmp = event[finishtime]
        tmp.insert(0, urgentJob)
        event[finishtime] = tmp
    except:
        event[finishtime] = [urgentJob]
    return reservedNodes
