class Job:
    def __init__(self, id, nodes, etime, memory, occurrenceTime):
        self.id = id
        self.nodes = nodes
        self.etime = etime
        self.memory = memory
        self.startTime = 0
        self.endTime = 0
        self.runNode = []
        self.status = -1
        self.occurrenceTime = occurrenceTime


class NormalJob(Job):
    def __init__(self, id, nodes, etime, memory, occurrenceTime):
        super().__init__(id, nodes, etime, memory, occurrenceTime)
        self.type = "normal"


class OndemandJob(Job):
    def __init__(self, id, nodes, etime, memory, occurrenceTime, deadlineTime):
        super().__init__(id, nodes, etime, memory, occurrenceTime)
        # 共通
        self.type = "ondemand"
        self.deadlineTime = deadlineTime
        self.totalPreemptionMemory = 0
        self.event = {}
        self.preemptionJobs = []
        self.startNodes = []


class InteractiveJob(OndemandJob):
    def __init__(self, id, nodes, etime, memory, occurrenceTime, deadlineTime):
        super().__init__(id, nodes, etime, memory, occurrenceTime, deadlineTime)
        self.type = "interactive"


class UrgentJob(OndemandJob):
    def __init__(self, id, nodes, etime, memory, occurrenceTime, deadlineTime):
        super().__init__(id, nodes, etime, memory, occurrenceTime, deadlineTime)
        self.type == "urgent"
