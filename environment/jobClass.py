class NormalJob:
    def __init__(self, id, nodes, etime, memory):
        self.type = "normal"
        self.id = id
        self.nodes = nodes
        self.etime = etime
        self.memory = memory
        self.startTime = 0
        self.endTime = 0
        self.runNode = []
        self.status = -1


class UrgentJob:
    def __init__(self, id, nodes, etime, memory, occurrenceTime, deadlineTime):
        # 共通
        self.type = "urgent"
        self.id = id
        self.nodes = nodes
        self.etime = etime
        self.memory = memory
        self.startTime = 0
        self.endTime = 0
        self.runNode = []
        self.status = -1
        self.occurrenceTime = occurrenceTime
        self.deadlineTime = deadlineTime
        self.totalPreemptionMemory = 0
        self.event = {}
        self.preemptionJobs = []
        self.startNodes = []
