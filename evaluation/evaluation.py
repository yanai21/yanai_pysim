def Makespan(result):
    makespan = result[-1][2]
    return makespan


def EnergyConsumption(electricPowerResult):
    energyConsumption = 0
    for electricPower in electricPowerResult:
        energyConsumption += electricPower
    return energyConsumption


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


def deadlineRatio(urgentJob_queue):
    count = 0
    for urgentJob in urgentJob_queue:
        if urgentJob.endTime <= urgentJob.deadlineTime:
            count += 1
    deadlineratio = count / len(urgentJob_queue)
    deadlineratio *= 100
    return deadlineratio
