from environment.jobClass import NormalJob,UrgentJob
from random import randint
import os
from environment.test.testSystem import testSystem
normalJob_queue = []
urgentJob_queue = []
event = {} #[node番号管理]
nodeMemory = testSystem.nodeMemory_mb

# #test用
# 通常ジョブ作成
for i in range(10):
    # id,nodes, etime,memory
    nodes = i+1
    etime = i+1
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
