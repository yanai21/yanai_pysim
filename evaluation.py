from system import idleEnergy_W,executionEnergy_W
def Makespan(result):
    makespan = result[-1][2] - result[0][1]
    print('メイクスパンは {} 秒'.format(makespan))
    return makespan
def EnergyConsumption(result,makespan,NUM_NODES,energyConsumption):
    #idleノード分割り当て
    totalIdleEnergyConsumption = idleEnergy_W * makespan * NUM_NODES
    energyConsumption += totalIdleEnergyConsumption
    for tmp in result:
        if("nodestart" in tmp[-1]):
            for node in tmp[3]:
                if(node >=NUM_NODES):
                    energyConsumption += executionEnergy_W
                else:
                    energyConsumption += (executionEnergy_W - idleEnergy_W)
        else:
            energyConsumption += (executionEnergy_W - idleEnergy_W) * len(tmp[3])
    print('消費電力は {} W'.format(energyConsumption))
