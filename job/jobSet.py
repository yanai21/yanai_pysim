from job.jobClass import NormalJob,UrgentJob
from random import randint
from system import nodeMemory
normalJob_queue = []
urgentJob_queue = []
event = {} #[node番号管理]

#通常ジョブ作成
for i in range(8):
    #id,nodes, etime,memory
    nodes = 2
    etime = i+1
    memory = nodeMemory * nodes *  randint(20,30) // 100
    job_tmp = NormalJob(i+1,nodes,etime,memory)
    normalJob_queue.append(job_tmp)
#緊急ジョブ作成
for i in range(1):
    #id,nodes, etime,memory,occurrenceTime,deadlineTime
    job_tmp = UrgentJob(-(i+1), 6, 10,i,1,660)
    urgentJob_queue.append(job_tmp) 
    #緊急ジョブの発生時刻をeventに追加
    try:
        event[job_tmp.occurrenceTime].append(job_tmp)
    except:
        event[job_tmp.occurrenceTime] = [job_tmp]

# #通常ジョブ作成
# for i in range(1000):
#     #id,nodes, etime,memory
#     nodes = randint(1,20)
#     etime = randint(10,100)
#     memory = nodeMemory * nodes *  randint(30,70) // 100
#     job_tmp = NormalJob(i+1,nodes,etime,memory)
#     normalJob_queue.append(job_tmp)
# #緊急ジョブ作成
# for i in range(1):
#     #id,nodes, etime,memory,occurrenceTime,deadlineTime
#     job_tmp = UrgentJob(-(i+1), 64, 600,i,1,660)
#     urgentJob_queue.append(job_tmp) 
#     #緊急ジョブの発生時刻をeventに追加
#     try:
#         event[job_tmp.occurrenceTime].append(job_tmp)
#     except:
#         event[job_tmp.occurrenceTime] = [job_tmp]