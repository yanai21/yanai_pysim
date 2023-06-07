from system import nodeStartTime,idleEnergy_W
from basicFunction import JobPlacement,FinishJob
from model import MultipleNodeStartup

def NodeStartList(NUM_SLEEP_NODES):
    nodeStartTimeList = [0]
    for i in range(1,NUM_SLEEP_NODES+1):
        startupTime = MultipleNodeStartup(i,MultipleNodeStartup=False)
        nodeStartTimeList.append(startupTime)
    return nodeStartTimeList


def NodeStart(use_nodes,NUM_Start_NODES,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,empty_node,Nodes,event):
    if(NUM_SLEEP_NODES >= NUM_Start_NODES):
        #node起動を用いたことを加える
        urgentJob.status.append("nodestart")
        #立ちあがったノード番号を記憶
        startNodes=[]
        for idx in range(NUM_NODES,NUM_NODES+NUM_Start_NODES):
            empty_node.append(idx)
            Nodes.append([])
            startNodes.append(idx)
        # now += nodeStartTime
        # empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=0)
    else:
        print("ノード起動できません")
        exit()
    return startNodes,empty_node,urgentJob,event,Nodes

def NodeShutdown(now,eventJob,Nodes,empty_node,result,startNodes,energyConsumption):
    #立ち上がったNodeをシャットダウン
    for idx in reversed(startNodes):
        empty_node.remove(idx)
        Nodes.pop(idx)
        energyConsumption += idleEnergy_W
    startNodes =[]
    return eventJob,Nodes,empty_node,result,startNodes,energyConsumption