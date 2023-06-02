import jobSet 
from basicFunction import JobPlacement,FinishJob
from preemptionAlgorithm import PreemptionAlgorithm,PreemptionRecover
from system import nodeStartTime
from nodeStartAlgorithm import NodeStart,NodeShutdown,NodeStartList
from killAlgorithm import KillAlgorithm

def main():
    NUM_NODES = 4
    NUM_SLEEP_NODES = 2
    Nodes = [[] for _ in range(NUM_NODES)]
    normalJob_queue = jobSet.normalJob_queue
    preemptionJobs=[]
    startNodes=[]
    normalJob_queue = jobSet.normalJob_queue
    urgentJob_queue = jobSet.urgentJob_queue
    event = jobSet.event
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
    #緊急ジョブの割り当て
    def UrgentJobAssignment(now,event,Nodes,empty_node,urgentJob,preemptionJobs,normalJob_queue):
        #ノードの確認
        available_num_node = len(empty_node)
        use_nodes = urgentJob.nodes
        #Idleノードに割り当て
        if available_num_node >= use_nodes:
            empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=0)
        #Idleノードに割り当てられない時
        else:
            #中断とノード起動のノード数を管理
            NUM_NODES_Preemption = 0
            NUM_NODES_NodeStart = 0
            #ノード起動に要する時間のテーブル化
            nodeStartTimeList = NodeStartList(NUM_SLEEP_NODES)
            
            #Preemption
            empty_node,urgentJob,event,Nodes,preemptionJobs=PreemptionAlgorithm(urgentJob,Nodes,NUM_NODES,available_num_node,use_nodes,now,event,empty_node)
            # #NodeStart
            # startNodes,empty_node,urgentJob,event,Nodes = NodeStart(use_nodes,available_num_node,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,empty_node,Nodes,event)
            # #Kill
            # empty_node,urgentJob,event,Nodes,normalJob_queue = KillAlgorithm(urgentJob,Nodes,NUM_NODES,available_num_node,use_nodes,now,event,empty_node,normalJob_queue)

        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        return event,Nodes,empty_node,preemptionJobs,startNodes,normalJob_queue

    

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
                event,Nodes,empty_node,preemptionJobs,startNodes,normalJob_queue=UrgentJobAssignment(now,event,Nodes,empty_node,eventJob,preemptionJobs,normalJob_queue)
            elif(eventJob.type=="urgent_p"):
                #結果書き込み、Nodesから排除
                eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result)    
                #復帰
                eventJob,Nodes,empty_node,preemptionJobs,event = PreemptionRecover(eventJob,Nodes,empty_node,now,preemptionJobs,event)
            elif(eventJob.type=="urgent_nodestart"):
                eventJob,Nodes,empty_node,result,startNodes = NodeShutdown(now,eventJob,Nodes,empty_node,result,startNodes)
            else:
                #結果書き込み、Nodesから排除
                eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result)   
        empty_node = sorted(empty_node)
        event,Nodes,empty_node,normalJob_queue=NormalJobAssignment(event,Nodes,empty_node,normalJob_queue)
                    

    print(result)

if __name__ == "__main__":
    main()