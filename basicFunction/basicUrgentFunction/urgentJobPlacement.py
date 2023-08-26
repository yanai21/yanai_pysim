def UrgentJobPlacement(now, urgentJob, event,system):
    if urgentJob.status == 0:
        etime = urgentJob.etime
        finish_time = now + etime
        urgentJob.startTime = now
        urgentJob.status = 1
        for node in urgentJob.runNode:
            if node.status == 2:
                node.status = 1
                node.setShutdownEvent(event,now,system)
            else:
                print("予約されたジョブを実行できない")
                exit()
        try:
            event[finish_time].append(urgentJob)
        except:
            event[finish_time] = [urgentJob]
    else:
        print("予約されたジョブを実行できない")
        exit()