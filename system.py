#システム情報
# aobaA={
# "NUM_NODES":576,
# "NUM_SLEEP_NODES" : 100,
# "writeBandwidth_MB" : 100,
# "readBandwidth_MB" : 100,
# "nodeStartTime_s" : 60,
# "nodeEndTime_s" : 120,
# "idleEnergy_W" : 60,
# "executionEnergy_W" : 210
# }

# #test用
# machine_id = 0
# NUM_NODES = 8
# NUM_SLEEP_NODES = 6
# #MB表記
# nodeMemory = 48 *1024
# #MB/s 表記
# writeBandwidth = 5000
# readBandwidth = 5000
# #s 表記
# nodeStartTime = 10
# nodeEndTime = 20
# idleEnergy_W = 60
# executionEnergy_W = 210

machine_id = 0
NUM_NODES = 576
NUM_SLEEP_NODES = int(NUM_NODES * (1-0.9))
#MB表記
nodeMemory = 48 *1024
#MB/s 表記
writeBandwidth = 5000
readBandwidth = 5000
#s 表記
nodeStartTime = 60
nodeEndTime = 120
idleEnergy_W = 60
executionEnergy_W = 210