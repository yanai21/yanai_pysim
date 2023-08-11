from basicFunction.basicFunction import JobPlacement, FinishJob


def NodeStart(urgentJob, Nodes, event, now, system):
    for node in urgentJob.startNodes:
        if node.status == -1:
            finishtime = now + system.nodeStartTime_s
            node.status = -21
            urgentJob.runNode.append(node)
        else:
            print("ノード起動できません")
            exit()
    try:
        urgentJob.event[finishtime].append("NodeStartFinish")
        event[finishtime].append(urgentJob)
    except:
        urgentJob.event[finishtime] = ["NodeStartFinish"]
        event[finishtime] = [urgentJob]


def NodeStartFinish(urgentJob):
    for node in urgentJob.startNodes:
        if node.status == -21:
            node.status = 2
        else:
            print("ノード起動を終了できない")
            exit()


def NodeShutdown(urgentJob, Nodes, event, now, system):
    for node in urgentJob.startNodes:
        if node.status == 0:
            finishtime = now + system.nodeEndTime_s
            node.status = -22
        else:
            print("ノード起動できません")
            exit()
    try:
        urgentJob.event[finishtime].append("NodeShutdownFinish")
        event[finishtime].append(urgentJob)
    except:
        urgentJob.event[finishtime] = ["NodeShutdownFinish"]
        event[finishtime] = [urgentJob]



def NodeShutdownFinish(urgentJob):
    for node in urgentJob.startNodes:
        if node.status == -22:
            node.status = -1
        else:
            print("ノードシャットダウンを終了できない")
            exit()
