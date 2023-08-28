from random import randint

# TODO:この実装はミスが起きやすい…
from environment.deploy.system import aoba_a

nodeMemory = aoba_a.nodeMemory_mb

normalJob_file_name = input("normalJob名")
urgentJob_file_name = input("urgentJob名")
folder = input("deploy or test?")
# 通常ジョブ作成
normalJobSet = "id,nodes,etime,memory,occurrenceTime"
for i in range(30):
    # id,nodes, etime,memory
    id = i + 1
    nodes = randint(3, 5)
    etime = randint(10, 100)
    memory = nodeMemory * nodes * randint(50, 70) // 100
    occurrenceTime = 0
    if i == 29:
        normalJobSet += "\n{},{},{},{},{}".format(id, nodes, etime, memory, 10)
    else:
        normalJobSet += "\n{},{},{},{},{}".format(id, nodes, etime, memory, occurrenceTime)
# 書き込み
with open("environment/{}/data/normalJob/{}_normalJob.txt".format(folder, normalJob_file_name), "w") as file:
    file.write(normalJobSet)

# 緊急ジョブ作成
urgentJobSet = "type,id,nodes,etime,occurrenceTime,deadlineTime"
for i in range(1):
    # type,id,nodes, etime,memory,occurrenceTime,deadlineTime
    type = "urgent"
    id = -(i + 1)
    nodes = 1
    etime = 200
    occurrenceTime = 50 + 3600 * i
    deadlineTime = occurrenceTime + etime + 300
    urgentJobSet += "\n{},{},{},{},{},{}".format(type, id, nodes, etime, occurrenceTime, deadlineTime)
# 書き込み
with open("environment/{}/data/urgentJob/{}_urgentJob.txt".format(folder, urgentJob_file_name), "w") as file:
    file.write(urgentJobSet)
