from job import NormalJob,UrgentJob
from basicFunction import JobPlacement,FinishJob
from model import PreemptionOverhead
from dynamicProgramming import DP



def main():
    #システム情報
    machine_id = 0
    writeBandwidth = 100
    readBandwidth = 50

    NUM_NODES = 4
    Nodes = [[] for _ in range(NUM_NODES)]
    normalJob_queue = []
    urgentJob_queue = []
    event = {} #[node番号管理]
    #通常ジョブ作成
    for i in range(4):
        #id,nodes, etime,memory
        job_tmp = NormalJob(i+1,1+i, 3,100)
        normalJob_queue.append(job_tmp)
    #緊急ジョブ作成
    for i in range(1):
        #id,nodes, etime,memory,occurrenceTime,deadlineTime
        job_tmp = UrgentJob(-(i+1), 3, 3,i,1,10)
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

            #ノードが空いているかの確認
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break
            #空いてるノードに配置
            if available_num_node >= use_nodes:
                empty_node,job,event,Nodes=JobPlacement(now,use_nodes,empty_node,job,event,Nodes,popNum=0)
                remove_idx.append(idx)
        #ジョブキューから配置したジョブを削除
        for idx in reversed(remove_idx):
            job_queue.pop(idx)
        
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)

        return event,Nodes,empty_node,job_queue

    def UrgentJobAssignment(now,event,Nodes,empty_node,urgentJob,preemptionJobs):
        #ノードの確認
        available_num_node = len(empty_node)
        use_nodes = urgentJob.nodes
        if available_num_node >= use_nodes:
            empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=0)
        #Preemption
        else:
            urgentJob.type = "urgent_p"
            #Nodesから投入されているジョブリストを作成
            jobSet = set()
            for job in Nodes:
                try:
                    jobSet.add(job[0])
                except:
                    pass
            jobList = list(jobSet)
            #DPの実行
            dp,breakdp=DP(len(jobList),NUM_NODES,jobList)
            #中断するジョブを選ぶ
            #ほしいノード数があるかの確認
            if(dp[-1][urgentJob.nodes - available_num_node]!=0):
                preemptionJobs=breakdp[-1][urgentJob.nodes - available_num_node]
            else:
                #最小のノード数を探索
                for i in range(urgentJob.nodes - available_num_node,NUM_NODES+1):
                    if(dp[-1][i]!=0):
                        preemptionJobs=breakdp[-1][i]
                        break
                    if(i==NUM_NODES):
                        print("中断できない")
                        exit()
            #中断開始
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
                #中断に要する時間を計測
                urgentJob.totalPreemptionMemory += preemptionJob.memory
            #Nodesから取り除く
            for idx in reversed(preemptionNode):
                Nodes[idx]=[]
                empty_node.append(idx)
            #緊急ジョブを割り当て (中断したジョブのノード数で実行するために、後ろから配列を参照する)
            # nowに中断時間を加える
            now += PreemptionOverhead(urgentJob.totalPreemptionMemory,writeBandwidth)
            empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=-1)
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        return event,Nodes,empty_node,preemptionJobs

    

    event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)


    while len(event) != 0:
        # #結果確認用
        # print(event)
        # print(Nodes)
        # print(empty_node)
        #終了ジョブをNodesから取り除く
        now=next(iter(event))
        eventJobs=event.pop(now)
        for eventJob in reversed(eventJobs):
            #緊急ジョブの投入かどうかを判断
            if(eventJob.type=="urgent" and eventJob.startTime==0):
                empty_node = sorted(empty_node)
                event,Nodes,empty_node,preemptionJobs=UrgentJobAssignment(now,event,Nodes,empty_node,eventJob,preemptionJobs)
            elif(eventJob.type=="urgent_p"):
                #結果書き込み、Nodesから排除
                eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result)    
                #復帰時間
                recover_time = PreemptionOverhead(eventJob.totalPreemptionMemory,readBandwidth)
                #中断ジョブを復帰
                for preemptionJob in preemptionJobs:
                    for idx in preemptionJob.runNode:
                        Nodes[idx]=[preemptionJob]
                        try:
                            empty_node.remove(idx)
                        except:
                            pass
                    finish_time = now + recover_time + preemptionJob.leftEtime
                    try:
                        event[finish_time].append(preemptionJob)
                    except:
                        event[finish_time] = [preemptionJob]
                    event = sorted(event.items())
                    event = dict((x, y) for x, y in event)
                preemptionJobs=[]
            else:
                #結果書き込み、Nodesから排除
                eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result)   
        empty_node = sorted(empty_node)
        event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
                    

    print(result)

if __name__ == "__main__":
    main()