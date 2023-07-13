#配置関数 (Nodesの追加、empty_nodeから取り出す、eventに追加)
def JobPlacement(now,empty_node, job, event, Nodes, popNum):
    etime = job.etime
    job.status = "run"
    finish_time = now + etime
    use_nodes = job.nodes
    for i in range(use_nodes):
        arrange_node_idx = empty_node.pop(popNum)
        if(Nodes[arrange_node_idx]==[]):
            Nodes[arrange_node_idx].append(job)
        else:
            print("割り当て不可")
            exit()
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
    
    
#終了したジョブ動作
def FinishJob(now,eventJob,Nodes,empty_node,result):
    #終了時刻記入
    eventJob.endTime=now
    eventJob.status = "finish"
    #結果書き込み
    result.append([eventJob.id,eventJob.startTime,eventJob.endTime,eventJob.runNode,eventJob.status,eventJob.method])
    #Nodesから取り除く
    for idx, node in enumerate(Nodes):
        #配列が空の可能性があるためtryを使う
        if(node == []):
            pass
        elif(eventJob==node[0]):
            Nodes[idx]=[]
            empty_node.append(idx)
    return empty_node

#通常ジョブのみで実行する際の引数用
def NormalJobPlacement():
    return