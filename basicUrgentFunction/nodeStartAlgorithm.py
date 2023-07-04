from system import nodeStartTime,idleEnergy_W,nodeEndTime
from basicFunction import JobPlacement,FinishJob
from model import MultipleNodeStartup

def NodeStartList(NUM_SLEEP_NODES):
    nodeStartTimeList = [0]
    for i in range(1,NUM_SLEEP_NODES+1):
        startupTime = MultipleNodeStartup(i,MultipleNodeStartup=False)
        nodeStartTimeList.append(startupTime)
    return nodeStartTimeList


def NodeStart(use_nodes,NUM_Start_NODES,NUM_SLEEP_NODES,NUM_NODES,urgentJob,now,empty_node,Nodes,event,resevedNodes):
    if(NUM_SLEEP_NODES >= NUM_Start_NODES):
        #node起動を用いたことを加える
        urgentJob.status.append("nodestart")
        #イベントに追加
        finishtime = now + nodeStartTime
        try:
            event[finishtime].afppend('nodeStart')
        except:
            event[finishtime] = ['nodeStart']
        #立ちあがったノード番号を記憶
        startNodes=[]
        for idx in range(NUM_NODES,NUM_NODES+NUM_Start_NODES):
            Nodes.append(['nodeStart'])
            startNodes.append(idx)
        # now += nodeStartTime
        # empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=0)
    else:
        print("ノード起動できません")
        exit()
    return startNodes,empty_node,urgentJob,event,Nodes,resevedNodes

def NodeStartFinish(Nodes,reservedNodes,startNodes):
    for idx in startNodes:
        reservedNodes.append(idx)
        Nodes[idx] = 'reserved'
    return Nodes,reservedNodes,startNodes
    



def NodeShutdown(now,eventJob,Nodes,empty_node,result,startNodes,energyConsumption,event):
    #立ち上がったNodeをシャットダウン
    for idx in reversed(startNodes):
        empty_node.remove(idx)
        Nodes[idx] = 'shutdown'
        #イベントに追加
        finishTime = now + nodeEndTime
        try:
            event[finishTime].append('shutdown')
        except:
            event[finishTime] = ['shutdown']
        energyConsumption += idleEnergy_W
    return eventJob,Nodes,empty_node,result,startNodes,energyConsumption,event
def NodeShutdownFinish(startNodes,Nodes):
    for idx in reversed(startNodes):
        Nodes.pop(idx)
    startNodes =[]
    return startNodes,Nodes