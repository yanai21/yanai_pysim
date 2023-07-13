if __name__ == "__main__":
    # print("提案手法")
    # main(True,ProposedUrgentJobAssignment)
    print("中断優先")
    preemptionMakespan,preemptionElectricPowerResult = main("preemption",True,PreemptionUrgentJobAssignment)
    print("ノード起動優先")
    nodeStartMakespan,nodeStartElectricPowerResult = main("nodeStart",True,NodeStartUrgentJobAssignment)
    print("通常ジョブのみ")
    normalJobMakespan,normalJobElectricPowerResult = main("normalJob",False,NormalJobPlacement)
    #グラフ
    MakeSpanGragh(normalJobMakespan,preemptionMakespan,nodeStartMakespan)
    ElectricPowerGragh(normalJobElectricPowerResult,preemptionElectricPowerResult,nodeStartElectricPowerResult)