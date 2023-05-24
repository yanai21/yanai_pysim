#モデル関数
def PreemptionOverhead(memory,bandwidth):
    overhead = memory // bandwidth
    return overhead
