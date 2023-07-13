# システム情報
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
class System:
    def __init__(self, systemNodes, sleep_ratio):
        # node関係
        self.systemNodes = systemNodes
        self.sleepNodes = int(systemNodes *  sleep_ratio)
        self.nodeMemory_mb = 48 * 1024
        #帯域幅
        self.writeBandwidth_mb = 5000
        self.readBandwidth_mb = 5000
        #起動時間
        self.nodeStartTime_s = 60
        self.nodeEndTime_s = 120
        #電力
        self.idleEnergy_w = 60
        self.executionEnergy_w = 210
