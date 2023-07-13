def UrgentJobPlacement(now,urgentJob,Nodes,event,reservedNodes):
    etime = urgentJob.etime
    finish_time = now + etime
    urgentJob.startTime=now
    urgentJob.eEndTime=finish_time
    urgentJob.status = "run"
    for idx in reservedNodes:
        Nodes[idx] = [urgentJob]
    try:
        event[finish_time].append(urgentJob)
    except:
        event[finish_time] = [urgentJob]
    reservedNodes = []
    return reservedNodes