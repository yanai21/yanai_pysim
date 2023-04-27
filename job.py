from random import randint
class NormalJob:
    def __init__(self,jobNum,excutionTimeMin,excutionTimeMax,nodeMin,nodeMax,memoryMin,memoryMax):
        self.jobNum=jobNum
        self.excutiTime=randint(excutionTimeMin,excutionTimeMax)
        self.node=randint(nodeMin,nodeMax)
        self.memory=randint(memoryMin,memoryMax)

class UrgentJob:
    pass