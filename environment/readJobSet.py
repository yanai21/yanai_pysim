from environment.jobClass import NormalJob, UrgentJob
from random import randint
import os
from environment.test.testSystem import testSystem

nodeMemory = testSystem.nodeMemory_mb


# #test用
def read_NormalJob(folder,file):
    with open("environment/{}/data/normalJob/{}_normalJob.txt".format(folder,file)) as f:
        normalJob_queue = []
        datas = f.readlines()
        for data in datas:
            data = data.replace("\n", "")
            joblist = data.split(",")
            if joblist[0] == "id":
                pass
            else:
                id = int(joblist[0])
                nodes = int(joblist[1])
                etime = int(joblist[2])
                try:
                    memory = int(joblist[3])
                except:
                    memory = nodeMemory * nodes
                job_tmp = NormalJob(id, nodes, etime, memory)
                normalJob_queue.append(job_tmp)
        return normalJob_queue


def read_UrgentJob(folder,file):
    with open("environment/{}/data/urgentJob/{}_urgentJob.txt".format(folder,file)) as f:
        urgentJob_queue = []
        event = {}
        datas = f.readlines()
        for data in datas:
            data = data.replace("\n", "")
            joblist = data.split(",")
            if joblist[0] == "id":
                pass
            else:
                id = int(joblist[0])
                nodes = int(joblist[1])
                etime = int(joblist[2])
                occurrenceTime = int(joblist[3])
                deadlineTime = int(joblist[4])
                memory = nodeMemory * nodes
                job_tmp = UrgentJob(id, nodes, etime, memory, occurrenceTime, deadlineTime)
                urgentJob_queue.append(job_tmp)
                # 緊急ジョブの発生時刻をeventに追加
                try:
                    event[job_tmp.occurrenceTime].append(job_tmp)
                except:
                    event[job_tmp.occurrenceTime] = [job_tmp]
        return urgentJob_queue, event

