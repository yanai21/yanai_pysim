class NormalJob():
    def __init__(self,id,nodes, etime,memory):
        self.type = "normal"
        self.leftEtime = 0
        self.eEndTime = 0
        self.id = id
        self.nodes = nodes
        self.etime = etime
        self.memory = memory
        self.startTime = 0
        self.endTime = 0
        self.runNode = []
        self.status = []
class UrgentJob():
    def __init__(self, id,nodes, etime,memory,occurrenceTime,deadlineTime):
        self.type = "urgent"
        self.id = id
        self.nodes = nodes
        self.etime = etime
        self.memory = memory
        self.occurrenceTime = occurrenceTime
        self.deadlineTime = deadlineTime
        self.startTime = 0
        self.endTime = 0
        self.runNode = []
        self.totalPreemptionMemory=0
        self.status = []