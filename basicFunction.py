#配置関数
def JobPlacement(now,use_nodes,empty_node,job,event,Nodes,popNum):
    etime = job.etime
    finish_time = now + etime
    for i in range(use_nodes):
        arrange_node_idx = empty_node.pop(popNum)
        Nodes[arrange_node_idx].append(job)
        #実行中のノードを書き込み
        job.runNode.append(arrange_node_idx)
        #start時刻の書き込み
        job.startTime=now
    try:
        job.eEndTime=finish_time
    except:
        pass

    try:
        event[finish_time].append(job)
    except:
        event[finish_time] = [job]
    
    return empty_node,job,event,Nodes
    
#終了したジョブ動作
def FinishJob(now,eventJob,Nodes,empty_node,result):
    #終了時刻記入
    eventJob.endTime=now
    #結果書き込み
    result.append([eventJob.id,eventJob.startTime,eventJob.endTime,eventJob.runNode,eventJob.status])
    #Nodesから取り除く
    for idx, node in enumerate(Nodes):
        try:
            if(eventJob.id==node[0].id):
                Nodes[idx]=[]
                empty_node.append(idx)
        except:
            pass   
    
    return eventJob,Nodes,empty_node,result