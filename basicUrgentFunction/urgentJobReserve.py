#開始時刻の追加
def UrgentReserve(urgentJob,empty_node,Nodes,event,reservedNodes,finishtime):
    #urgentNodesのStatusの変更
    etime = urgentJob.etime
    use_nodes = urgentJob.nodes
    urgentJob.status = "reserved"
    for i in range(use_nodes):
        arrange_node_idx = empty_node.pop(-1)
        if(Nodes[arrange_node_idx]==[]):
            Nodes[arrange_node_idx] = ["reserved"]
        reservedNodes.append(arrange_node_idx)
        #予約ノードを書き込み
        urgentJob.runNode.append(arrange_node_idx)
    #eventの追加
    try:
        tmp = event[finishtime]
        tmp.insert(0,urgentJob)
        event[finishtime] = tmp
    except:
        event[finishtime] = [urgentJob]
