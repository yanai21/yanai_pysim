from job import NormalJob,UrgentJob

def main():
    machine_id = 0
    NUM_NODES = 4
    Nodes = [[] for _ in range(NUM_NODES)]
    normalJob_queue = []
    urgentJob_queue = []
    event = {} #[node番号管理]
    #通常ジョブ作成
    for i in range(3):
        #id,nodes, etime,memory
        job_tmp = NormalJob(i+1,i+1, 3,i)
        normalJob_queue.append(job_tmp)
    #緊急ジョブ作成
    for i in range(1):
        #id,nodes, etime,memory,occurrenceTime,deadlineTime
        job_tmp = UrgentJob(-(i+1), 2, 3,i,1,10)
        urgentJob_queue.append(job_tmp) 
        #緊急ジョブの発生時刻をeventに追加
        try:
            event[job_tmp.occurrenceTime].append(job_tmp)
        except:
            event[job_tmp.occurrenceTime] = [job_tmp]
    now = 0
    empty_node = [i for i in range(NUM_NODES)]
    result=[]
    preemptionJobs=[]


    def NormalJobAssignment(event,Nodes,empty_node,job_queue):
        remove_idx = []
        for idx, job in enumerate(job_queue):
            use_nodes = job.nodes
            etime = job.etime
            finish_time = now + etime

            #空いてるノードに配置
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break

            if available_num_node >= use_nodes:
                for i in range(use_nodes):
                    arrange_node_idx = empty_node.pop(0)
                    Nodes[arrange_node_idx].append(job)
                    #実行中のノードを書き込み
                    job.runNode.append(arrange_node_idx)
                    #start時刻の書き込み
                    job.startTime=now
                    job.eEndTime=finish_time
            
                try:
                    event[finish_time].append(job)
                except:
                    event[finish_time] = [job]

                remove_idx.append(idx)
        
        for idx in reversed(remove_idx):
            job_queue.pop(idx)
        
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        return event,Nodes,empty_node,job_queue
    def UrgentJobAssignment(event,Nodes,empty_node,urgentJob,preemptionJobs):
        #ノードの確認
        available_num_node = len(empty_node)
        use_nodes = urgentJob.nodes
        etime = urgentJob.etime
        finish_time = now + etime
        if available_num_node >= use_nodes:
            for i in range(use_nodes):
                arrange_node_idx = empty_node.pop(0)
                Nodes[arrange_node_idx].append(urgentJob)
                #実行中のノードを書き込み
                urgentJob.runNode.append(arrange_node_idx)
                #start時刻の書き込み
                urgentJob.startTime=now
        else:
            #Prremption
            urgentJob.type = "urgent_p"
            preemptionJobs=Nodes[1]
            preemptionNode=[]
            for preemptionJob in preemptionJobs:
                #残り時間の計測
                preemptionJob.leftEtime = preemptionJob.etime - now
                #中断ジョブをeventから削除
                event_tmp = event[preemptionJob.eEndTime]
                event_tmp.remove(preemptionJob)
                event[preemptionJob.eEndTime] = event_tmp
                #中断した結果、空いたノードの把握
                preemptionNode.extend(preemptionJob.runNode)
            #Nodesから取り除く
            for idx in reversed(preemptionNode):
                Nodes[idx]=[]
                empty_node.append(idx)
            #緊急ジョブを割り当て
            empty_node[0:0] = preemptionNode
            for i in range(use_nodes):
                arrange_node_idx = empty_node.pop(-1)
                Nodes[arrange_node_idx].append(urgentJob)
                #実行中のノードを書き込み
                urgentJob.runNode.append(arrange_node_idx)
                #start時刻の書き込み
                urgentJob.startTime=now
        try:
            event[finish_time].append(urgentJob)
        except:
            event[finish_time] = [urgentJob]
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        return event,Nodes,empty_node,preemptionJobs

    event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)


    while len(event) != 0:
        #結果確認用
        print(event)
        # print(Nodes)
        # print(empty_node)
        #終了ジョブをNodesから取り除く
        now=next(iter(event))
        eventJobs=event.pop(now)
        for eventJob in reversed(eventJobs):
            #緊急ジョブの投入かどうかを判断
            if(eventJob.type=="urgent" and eventJob.startTime==0):
                empty_node = sorted(empty_node)
                event,Nodes,empty_node,preemptionJobs=UrgentJobAssignment(event,Nodes,empty_node,eventJob,preemptionJobs)
            else:
                #終了時刻記入
                eventJob.endTime=now
                #結果書き込み
                result.append([eventJob.id,eventJob.startTime,eventJob.endTime,eventJob.runNode])
                #Nodesから取り除く
                for idx, node in enumerate(Nodes):
                    try:
                        if(eventJob.id==node[0].id):
                            Nodes[idx]=[]
                            empty_node.append(idx)
                    except:
                        pass
                if(eventJob.type=="urgent_p"):
                    #中断ジョブを復帰
                    print(preemptionJobs)
                    for preemptionJob in preemptionJobs:
                        for idx in preemptionJob.runNode:
                            Nodes[idx]=preemptionJob
                            empty_node.remove(idx)
                        finish_time = now + preemptionJob.leftEtime
                        try:
                            event[finish_time].append(preemptionJob)
                        except:
                            event[finish_time] = [preemptionJob]
                        event = sorted(event.items())
                        event = dict((x, y) for x, y in event)
        empty_node = sorted(empty_node)
        event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)

    print(result)

if __name__ == "__main__":
    main()