from environment.jobClass import NormalJob, UrgentJob
from random import randint
import os


class Environment:
    def __init__(self, system, folder, normalJob_file, urgentJob_file):
        self.system = system
        self.event = {}
        self.normalJob_queue = []
        self.urgentJob_queue = []
        self.folder = folder
        self.normalJob_file = normalJob_file
        self.urgentJob_file = urgentJob_file
        self.read_NormalJob(folder, normalJob_file)
        self.read_UrgentJob(folder, urgentJob_file)

    def read_NormalJob(self, folder, file):
        with open("environment/{}/data/normalJob/{}_normalJob.txt".format(folder, file)) as f:
            self.normalJob_queue = []
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
                    memory = int(joblist[3])
                    occurrenceTime = int(joblist[4])
                    job_tmp = NormalJob(id, nodes, etime, memory, occurrenceTime)
                    if occurrenceTime == 0:
                        self.normalJob_queue.append(job_tmp)
                    else:
                        try:
                            self.event[job_tmp.occurrenceTime].append(job_tmp)
                        except:
                            self.event[job_tmp.occurrenceTime] = [job_tmp]

    def read_UrgentJob(self, folder, file):
        with open("environment/{}/data/urgentJob/{}_urgentJob.txt".format(folder, file)) as f:
            self.urgentJob_queue = []
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
                    memory = self.system.nodeMemory_mb * nodes
                    job_tmp = UrgentJob(id, nodes, etime, memory, occurrenceTime, deadlineTime)
                    self.urgentJob_queue.append(job_tmp)
                    # 緊急ジョブの発生時刻をeventに追加
                    try:
                        self.event[job_tmp.occurrenceTime].append(job_tmp)
                    except:
                        self.event[job_tmp.occurrenceTime] = [job_tmp]
