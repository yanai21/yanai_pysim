from job.jobClass import NormalJob,UrgentJob
normalJob_queue = []
urgentJob_queue = []
event = {} #[node番号管理]

#通常ジョブ作成
for i in range(5):
    #id,nodes, etime,memory
    job_tmp = NormalJob(i+1,i+1,3,100*(i+1))
    normalJob_queue.append(job_tmp)
#緊急ジョブ作成
for i in range(1):
    #id,nodes, etime,memory,occurrenceTime,deadlineTime
    job_tmp = UrgentJob(-(i+1), 3, 3,i,1,10)
    urgentJob_queue.append(job_tmp) 
    #緊急ジョブの発生時刻をeventに追加
    try:
        event[job_tmp.occurrenceTime].append(job_tmp)
    except:
        event[job_tmp.occurrenceTime] = [job_tmp]