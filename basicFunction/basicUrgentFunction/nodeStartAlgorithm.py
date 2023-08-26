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

