from jobClass import NormalJob,UrgentJob
from random import randint
from testSystem import test1
normalJob_queue = []
urgentJob_queue = []
event = {} #[node番号管理]
nodeMemory = test1.nodeMemory_mb

# #test用
# 通常ジョブ作成
for i in range(100):
    # id,nodes, etime,memory
    nodes = randint(1,4)
    etime = randint(100,1000)
    memory = nodeMemory * nodes
    job_tmp = NormalJob(i + 1, nodes, etime, memory)
    normalJob_queue.append(job_tmp)
# 緊急ジョブ作成
for i in range(1):
    # id,nodes, etime,memory,occurrenceTime,deadlineTime
    occurrenceTime = 10 + 3600*i
    job_tmp = UrgentJob(-(i + 1), 1, 600, i,occurrenceTime,occurrenceTime+600)
    urgentJob_queue.append(job_tmp)
    # 緊急ジョブの発生時刻をeventに追加
    try:
        event[job_tmp.occurrenceTime].append(job_tmp)
    except:
        event[job_tmp.occurrenceTime] = [job_tmp]
