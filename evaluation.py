from system import idleEnergy_W,executionEnergy_W
def Makespan(result):
    makespan = result[-1][2] - result[0][1]
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
    return energyConsumption
def ElectricPower(electricPowerResult,now,Nodes):
    electricPower = 0
    for node in Nodes:
        if(len(node) ==0):
            electricPower += idleEnergy_W
        elif(node[0] == "preemption" or node[0] == "recover"):
            electricPower += executionEnergy_W
        elif(type(node[0]) == str):
            electricPower += idleEnergy_W

        else:
            electricPower += executionEnergy_W

    if(now == len(electricPowerResult)):
        electricPowerResult.append(electricPower)
    else:
        addNum = now - len(electricPowerResult)
        for i in range(addNum +1):
            electricPowerResult.append(electricPower)
    return electricPowerResult
