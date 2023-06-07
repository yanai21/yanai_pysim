from basicFunction import JobPlacement
from basicUrgentFunction.preemptionAlgorithm import PreemptionAlgorithm,DP
from system import nodeStartTime,writeBandwidth,idleEnergy_W,NUM_NODES,NUM_SLEEP_NODES
from basicUrgentFunction.nodeStartAlgorithm import NodeStart
from model import PreemptionOverhead

#緊急ジョブの割り当て
def ProposedUrgentJobAssignment(now,event,Nodes,empty_node,urgentJob,preemptionJobs,normalJob_queue,startNodes,result,energyConsumption):
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
        #中断もしくは起動に要する時間
        overheadTime = 0
        #中断に要するテーブルの作成
        #Nodesから投入されているジョブリストを作成
        jobSet = set()
        for job in Nodes:
            try:
                jobSet.add(job[0])
            except:
                pass
        jobList = list(jobSet)
        dp,breakdp=DP(len(jobList),NUM_NODES,jobList)
        #必要なノード数の把握
        NUM_NEED_NODES = use_nodes - available_num_node
        #全探索
        for i in range(NUM_SLEEP_NODES+1):
            if(i==0):
                for j in range(NUM_NEED_NODES,NUM_NODES+1):
                    if(dp[-1][j]!=0):
                        NUM_NODES_Preemption = j
                        overheadTime = PreemptionOverhead(dp[-1][j],writeBandwidth)
                        break
            else:
                tmpOverheadTime = max(nodeStartTime,PreemptionOverhead(dp[-1][NUM_NEED_NODES - i],writeBandwidth))
                if(tmpOverheadTime <overheadTime):
                    overheadTime = tmpOverheadTime
                    NUM_NODES_NodeStart = i
                    NUM_NODES_Preemption = NUM_NEED_NODES - i
        print(NUM_NODES_Preemption)
        print(NUM_NODES_NodeStart)
        #Preemption
        if(NUM_NODES_Preemption != 0):
            preemptionJobs = breakdp[-1][NUM_NODES_Preemption]
            empty_node,urgentJob,event,Nodes,preemptionJobs,result=PreemptionAlgorithm(urgentJob,Nodes,use_nodes,now,event,empty_node,preemptionJobs,result)
        #NodeStart
        if(NUM_NODES_NodeStart !=0):
            startNodes,empty_node,urgentJob,event,Nodes = NodeStart(use_nodes,NUM_NODES_NodeStart,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,empty_node,Nodes,event)
            energyConsumption += NUM_NODES_NodeStart * overheadTime * idleEnergy_W
        #配置：JobPlacement
        now += overheadTime
        empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=-1)
        #kill
        # empty_node,urgentJob,event,Nodes,normalJob_queue = KillAlgorithm(urgentJob,Nodes,NUM_NODES,available_num_node,use_nodes,now,event,empty_node,normalJob_queue)

    event = sorted(event.items())
    event = dict((x, y) for x, y in event)
    return event,Nodes,empty_node,preemptionJobs,startNodes,normalJob_queue,result,energyConsumption