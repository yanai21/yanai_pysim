def Makespan(result):
    makespan = result[-1][2]
    return makespan


# def EnergyConsumption(result,makespan,,energyConsumption):
#     #idleノード分割り当て
#     totalIdleEnergyConsumption = idleEnergy_W * makespan * NUM_NODES
#     energyConsumption += totalIdleEnergyConsumption
#     for tmp in result:
#         if("nodestart" in tmp[-1]):
#             for node in tmp[3]:
#                 if(node >=NUM_NODES):
#                     energyConsumption += executionEnergy_W
#                 else:
#                     energyConsumption += (executionEnergy_W - idleEnergy_W)
#         else:
#             energyConsumption += (executionEnergy_W - idleEnergy_W) * len(tmp[3])
#     print('消費電力は {} W'.format(energyConsumption))
#     return energyConsumption
def ElectricPower(electricPowerResult, now, Nodes, system):
    electricPower = 0
    for node in Nodes:
        if node.status == -1:
            pass
        elif node.status == 0 or node.status == 2:
            electricPower += system.idleEnergy_w
        else:
            electricPower += system.executionEnergy_w
    if now == len(electricPowerResult):
        electricPowerResult.append(electricPower)
    else:
        addNum = now - len(electricPowerResult)
        for i in range(addNum + 1):
            electricPowerResult.append(electricPower)
    return electricPowerResult
