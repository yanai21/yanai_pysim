from random import randint
class NormalJob:
    def __init__(self,idstart,jobNum,excutionTimeMin,excutionTimeMax,nodeMin,nodeMax,memoryMin,memoryMax):
        self.idstart=idstart
        self.jobNum=jobNum
        self.excutionTimeMin=excutionTimeMin
        self.excutionTimeMax=excutionTimeMax
        self.nodeMin=nodeMin
        self.nodeMax=nodeMax
        self.memoryMin=memoryMin
        self.memoryMax=memoryMax
    def DataCreate(self):
        normalJobQueue=[]
        for i in range(self.jobNum):
            excutionTime=randint(self.excutionTimeMin,self.excutionTimeMax)
            node=randint(self.nodeMin,self.nodeMax)
            memory=randint(self.memoryMin,self.memoryMax)
            normalJobQueue.append([self.idstart+i,excutionTime,node,memory])
        return normalJobQueue
class UrgentJob:
    pass