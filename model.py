from system import nodeStartTime
#モデル関数
def PreemptionOverhead(memory,bandwidth):
    overhead = memory // bandwidth
    return overhead

def MultipleNodeStartup(num_job,MultipleNodeStartup):
    #重み
    weight = 0.1
    if(MultipleNodeStartup):
        startupTime  = (1 +num_job * weight) * nodeStartTime
    else:
        startupTime = nodeStartTime
    return int(startupTime)
