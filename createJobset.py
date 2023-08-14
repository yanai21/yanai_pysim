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
for i in range(100):
    #id,nodes, etime,memory
    id = i+1
    nodes = randint(1,64)
    etime = randint(100,1000)
    memory = nodeMemory * nodes *  randint(30,70) // 100
    normalJobSet += "\n{},{},{},{}".format(id,nodes,etime,memory)
#書き込み
with open("environment/{}/data/normalJob/{}_normalJob.txt".format(folder,normalJob_file_name),'w') as file:
    file.write(normalJobSet)

#緊急ジョブ作成
urgentJobSet = "id,nodes,etime,occurrenceTime,deadlineTime"
for i in range(2):
    #id,nodes, etime,memory,occurrenceTime,deadlineTime
    occurrenceTime = 100 + 1000*i
    id = - (i+1)
    nodes = 64
    etime = 600
    deadlineTime = occurrenceTime + etime + 300
    urgentJobSet += "\n{},{},{},{},{}".format(id,nodes,etime,occurrenceTime,deadlineTime)
#書き込み
with open("environment/{}/data/urgentJob/{}_urgentJob.txt".format(folder,urgentJob_file_name),'w') as file:
    file.write(urgentJobSet)