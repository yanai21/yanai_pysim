from environment.jobClass import NormalJob, UrgentJob, InteractiveJob
from random import randint
import os


class Environment:
    def __init__(self, system, folder, normalJob_file, urgentJob_file):
        self.system = system
        self.event = {}
        # 通常ジョブを格納するもの
        self.normalJob_queue = []
        # 緊急ジョブを格納しておくもの
        self.urgentJob_queue = []
        self.folder = folder
        self.normalJob_file = normalJob_file
        self.urgentJob_file = urgentJob_file
        self.read_NormalJob(folder, normalJob_file)
        self.read_UrgentJob(folder, urgentJob_file)

    def read_NormalJob(self, folder, file):
        with open("environment/{}/data/normalJob/{}_normalJob.txt".format(folder, file)) as f:
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
                    self.normalJob_queue.append(job_tmp)
                    if occurrenceTime != 0:
                        try:
                            self.event[job_tmp.occurrenceTime].append(job_tmp)
                        except:
                            self.event[job_tmp.occurrenceTime] = [job_tmp]

    def read_UrgentJob(self, folder, file):
        with open("environment/{}/data/urgentJob/{}_urgentJob.txt".format(folder, file)) as f:
            datas = f.readlines()
            for data in datas:
                data = data.replace("\n", "")
                joblist = data.split(",")
                if joblist[0] == "type":
                    pass
                else:
                    type = joblist[0]
                    id = int(joblist[1])
                    nodes = int(joblist[2])
                    etime = int(joblist[3])
                    occurrenceTime = int(joblist[4])
                    deadlineTime = int(joblist[5])
                    memory = self.system.nodeMemory_mb * nodes
                    if type == "urgent":
                        job_tmp = UrgentJob(id, nodes, etime, memory, occurrenceTime, deadlineTime)
                    else:
                        job_tmp = InteractiveJob(id, nodes, etime, memory, occurrenceTime, deadlineTime)
                    self.urgentJob_queue.append(job_tmp)
                    # 緊急ジョブの発生時刻をeventに追加
                    try:
                        self.event[job_tmp.occurrenceTime].append(job_tmp)
                    except:
                        self.event[job_tmp.occurrenceTime] = [job_tmp]
