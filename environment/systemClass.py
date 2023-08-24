class System:
    def __init__(self, systemNodes, sleep_ratio, maxIdleTime):
        # node関係
        self.systemNodes = systemNodes
        self.sleepNodes = int(systemNodes * sleep_ratio)
        self.nodeMemory_mb = 48 * 1024
        # 帯域幅
        self.writeBandwidth_mb = 5000
        self.readBandwidth_mb = 5000
        # 起動時間
        self.nodeStartTime_s = 60
        self.nodeEndTime_s = 120
        # 電力
        self.idleEnergy_w = 60
        self.executionEnergy_w = 210
        # 最大アイドル時間
        self.maxIdleTime = maxIdleTime

    def preemptionOverhead(self, memory, bandwidth):
        overhead = memory // bandwidth
        return overhead
