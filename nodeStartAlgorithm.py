from system import nodeStartTime
from basicFunction import JobPlacement,FinishJob

def NodeStart(use_nodes,available_num_node,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,empty_node,Nodes,event):
    NUM_Start_NODES = use_nodes - available_num_node
    if(NUM_SLEEP_NODES >= NUM_Start_NODES):
        #node起動を用いたことを加える
        urgentJob.type = "urgent_nodestart"
        #立ちあがったノード番号を記憶
        startNodes=[]
        for idx in range(NUM_NODES,NUM_NODES+NUM_Start_NODES):
            empty_node.append(idx)
            Nodes.append([])
            startNodes.append(idx)
        now += nodeStartTime
        empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=0)
    else:
        print("ノード起動できません")
        exit()
    return startNodes,empty_node,urgentJob,event,Nodes

def NodeShutdown(now,eventJob,Nodes,empty_node,result,startNodes):
    #結果書き込み、Nodesから排除
    eventJob,Nodes,empty_node,result=FinishJob(now,eventJob,Nodes,empty_node,result)
    #立ち上がったNodeをシャットダウン
    for idx in reversed(startNodes):
        empty_node.remove(idx)
        Nodes.pop(idx)
    startNodes =[]
    return eventJob,Nodes,empty_node,result,startNodes