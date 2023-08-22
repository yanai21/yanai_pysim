from random import randint
from environment.deploy.system import aoba_a
normalJob_queue = []
urgentJob_queue = []
event = {} #[node番号管理]
nodeMemory = aoba_a.nodeMemory_mb

normalJob_file_name = input("normalJob名")
urgentJob_file_name = input("urgentJob名")
folder = input("deploy or test?")
#通常ジョブ作成
normalJobSet = "id,nodes,etime,memory"
for i in range(1000):
    #id,nodes, etime,memory
    id = i+1
    nodes = randint(1,30)
    etime = randint(600,7200)
    memory = nodeMemory * nodes *  randint(50,70) // 100
    normalJobSet += "\n{},{},{},{}".format(id,nodes,etime,memory)
#書き込み
with open("environment/{}/data/normalJob/{}_normalJob.txt".format(folder,normalJob_file_name),'w') as file:
    file.write(normalJobSet)

#緊急ジョブ作成
urgentJobSet = "id,nodes,etime,occurrenceTime,deadlineTime"
for i in range(5):
    #id,nodes, etime,memory,occurrenceTime,deadlineTime
    occurrenceTime = 50 + 3600*i
    id = - (i+1)
    nodes = 50
    etime = 900
    deadlineTime = occurrenceTime + etime + 300
    urgentJobSet += "\n{},{},{},{},{}".format(id,nodes,etime,occurrenceTime,deadlineTime)
#書き込み
with open("environment/{}/data/urgentJob/{}_urgentJob.txt".format(folder,urgentJob_file_name),'w') as file:
    file.write(urgentJobSet)