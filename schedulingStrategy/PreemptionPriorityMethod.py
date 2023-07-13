from basicFunction import JobPlacement
from basicUrgentFunction.preemptionAlgorithm import PreemptionAlgorithm,DP
from environment.class.system import nodeStartTime,writeBandwidth,idleEnergy_W,NUM_NODES,NUM_SLEEP_NODES
from basicUrgentFunction.nodeStartAlgorithm import NodeStart
from basicUrgentFunction.urgentJobReserve import UrgentReserve
from model import PreemptionOverhead

#緊急ジョブの割り当て
def PreemptionUrgentJobAssignment(Nodes,empty_node,preemptionJobs,startNodes,reservedNodes,preemptionNodes,now,urgentJob,event,result):
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
        for i in range(NUM_NEED_NODES,len(dp[-1])):
            if(dp[-1][i]!=0):
                NUM_NODES_Preemption = i
                overheadTime = PreemptionOverhead(dp[-1][i],writeBandwidth)
                break
        print("PreemptionNodes:{}".format(NUM_NODES_Preemption))
        print("NodeStartNodes:{}".format(NUM_NODES_NodeStart))
        #Preemption
        if(NUM_NODES_Preemption != 0):
            preemptionJobs = breakdp[-1][NUM_NODES_Preemption]
            preemptionJobs,preemptionNodes,reservedNodes = PreemptionAlgorithm(urgentJob,Nodes,now,event,preemptionJobs,preemptionNodes,result,reservedNodes)
        #NodeStart
        if(NUM_NODES_NodeStart !=0):
            startNodes,reservedNodes=NodeStart(NUM_NODES_NodeStart,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,Nodes,event,startNodes,reservedNodes)
        #緊急ジョブの割り当て時刻の決定
        finishtime = now + overheadTime
        #緊急ジョブを割り当てるノードの予約
        reservedNodes = UrgentReserve(urgentJob,empty_node,Nodes,event,reservedNodes,finishtime)
    return preemptionJobs,startNodes,reservedNodes,preemptionNodes