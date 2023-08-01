def UrgentJobPlacement(now, urgentJob,event):
    if urgentJob.status == 0:
        etime = urgentJob.etime
        finish_time = now + etime
        urgentJob.startTime = now
        urgentJob.status = 1
        for node in urgentJob.runNode:
            if node.status ==2:
                node.status =1
            else:
                print("予約されたジョブを実行できない")
                exit()
        try:
            event[finish_time].append(urgentJob)
        except:
            event[finish_time] = [urgentJob]
    else:
        print("予約されたジョブを実行できない")
        exit()


def UrgentReserve(urgentJob, Nodes, event, finishtime, now):
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
