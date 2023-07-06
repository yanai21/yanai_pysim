from basicFunction import JobPlacement
from basicUrgentFunction.preemptionAlgorithm import PreemptionAlgorithm,DP
from system import nodeStartTime,writeBandwidth,idleEnergy_W,NUM_NODES,NUM_SLEEP_NODES
from basicUrgentFunction.nodeStartAlgorithm import NodeStart
from basicUrgentFunction.urgentJobReserve import UrgentReserve
from model import PreemptionOverhead

#緊急ジョブの割り当て
def NodeStartUrgentJobAssignment(Nodes,empty_node,preemptionJobs,startNodes,reservedNodes,now,urgentJob,event,result):
    #ノードの確認
    available_num_node = len(empty_node)
    use_nodes = urgentJob.nodes
    #Idleノードに割り当て
    if available_num_node >= use_nodes:
        JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=0)
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
        if(NUM_NEED_NODES <= NUM_SLEEP_NODES):
            NUM_NODES_NodeStart = NUM_NEED_NODES
            overheadTime = nodeStartTime
        else:
            NUM_NODES_NodeStart = NUM_SLEEP_NODES
            NUM_NEED_NODES -= NUM_SLEEP_NODES
            for i in range(NUM_NEED_NODES,NUM_NODES+1):
                if(dp[-1][i]!=0):
                    NUM_NODES_Preemption = i
                    overheadTime = max(nodeStartTime,PreemptionOverhead(dp[-1][i],writeBandwidth))
                    break
        print(NUM_NODES_Preemption)
        print(NUM_NODES_NodeStart)
        #Preemption
        if(NUM_NODES_Preemption != 0):
            #TODO:eventに追加
            preemptionJobs = breakdp[-1][NUM_NODES_Preemption]
            empty_node,urgentJob,event,Nodes,preemptionJobs,result=PreemptionAlgorithm(urgentJob,Nodes,use_nodes,now,event,empty_node,preemptionJobs,result)
        #NodeStart
        if(NUM_NODES_NodeStart !=0):
            #TODO:eventに追加
            NodeStart(NUM_NODES_NodeStart,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,empty_node,Nodes,event,startNodes)
        #緊急ジョブの割り当て時刻の決定
        finishtime = now + overheadTime
        #緊急ジョブを割り当てるノードの予約
        UrgentReserve(urgentJob,empty_node,Nodes,event,reservedNodes,finishtime)

    event = sorted(event.items())
    event = dict((x, y) for x, y in event)