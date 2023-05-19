

def main():
    
    class Job():
        def __init__(self, id, pred_etime, nodes, etime,memory,startTime,endTime,runNode):
            self.id = id
            self.pred_etime = pred_etime
            self.nodes = nodes
            self.etime = etime
            self.memory = memory
            self.startTime = startTime
            self.endTime = endTime
            self.runNode = runNode

    machine_id = 0
    NUM_NODES = 4
    Nodes = [[] for _ in range(NUM_NODES)]
    job_queue = []
    event = {} #[node番号管理]
    #ジョブ作成
    for i in range(3):
        job_tmp = Job(i, 3, i+1, 3,i,0,0,[])
        job_queue.append(job_tmp)
    now = 0
    empty_node = [i for i in range(NUM_NODES)]
    result=[]


    def JobAssignment(event,Nodes,empty_node,job_queue):
        remove_idx = []
        for idx, job in enumerate(job_queue):
            job_id = job.id
            use_nodes = job.nodes
            # pred_etime = job.pred_etime
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

    JobAssignment(event,Nodes,empty_node,job_queue)




    while len(event) != 0:
        #結果確認用
        print(event)
        print(Nodes)
        print(empty_node)
        #終了ジョブをNodesから取り除く
        now=next(iter(event))
        finish_jobs=event.pop(now)
        for finishJob in finish_jobs:
            #終了時刻記入
            finishJob.endTime=now
            #結果書き込み
            result.append([finishJob.id,finishJob.startTime,finishJob.endTime,finishJob.runNode])

            #Nodesから取り除く
            for idx, node in enumerate(Nodes):
                try:
                    if(finishJob.id==node[0].id):
                        Nodes[idx]=[]
                        empty_node.append(idx)
                except:
                    pass
        empty_node = sorted(empty_node)
        JobAssignment(event,Nodes,empty_node,job_queue)
    #     #node情報を書き込むout.csv
    #     array_tmp = []
    #     for node in Nodes:
    #         array_tmp.append(node[0].id)
    #     #dfに追加

    #     #配置関数

    print(result)

if __name__ == "__main__":
    main()