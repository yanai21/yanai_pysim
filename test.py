from scheduling import scheduling

from schedulingStrategy.NodeStartPriorityMetod import NodeStartPriorityAlgorithm
from schedulingStrategy.PreemptionPriorityMethod import PreemptionPriorityAlgorithm
from schedulingStrategy.Randompreemption import RandomPreemptionAlgorithm
from basicFunction.basicFunction import NormalJobPlacement
from schedulingStrategy.ProposedMethod import ProposedAlgorithm
from environment.testEnvironment import (
    test1_environment,
    test2_environment,
    test3_environment,
    test4_environment,
    test5_environment,
    aoba_test1_environment,
    aoba_test2_environment,
    aoba_tradeoff_environment,
    aoba_deploy1_environment
)
from evaluation.gragh import MakeSpanGragh, ElectricPowerGragh, EnergyConsumptionGragh, deadlineRatioGragh

environment = aoba_test1_environment
# print("中断優先")
# preemptionMakespan, preemptionElectricPowerResult, preemptionEnergyConsumption, preemptionDeadlineRatio = scheduling(
#     "preemption", True, PreemptionPriorityAlgorithm, environment
# )
print("ノード起動優先")
nodeStartMakespan, nodeStartElectricPowerResult, nodeStartEnergyConsumption, nodeStartDeadlineRatio = scheduling(
    "nodeStart", True, NodeStartPriorityAlgorithm, environment
)
print("通常ジョブのみ")
normalJobMakespan, normalJobElectricPowerResult, normalJobEnergyConsumption, normakJobDeadlineRatio = scheduling(
    "normalJob", False, NormalJobPlacement, environment
)
# print("ランダム選択手法")
# randomMakespan, randomElectricPowerResult, randomEnergyConsumption, randomDeadlineRatio = scheduling(
#     "random", True, RandomPreemptionAlgorithm, environment
# )
# print("提案手法")
# proposedMakespan, proposedElectricPowerResult, proposedEnergyConsumption, proposedDeadlineRatio = scheduling(
#     "proposed", True, ProposedAlgorithm, environment
# )
# # # # グラフ
# MakeSpanGragh(proposedMakespan, randomMakespan, preemptionMakespan, nodeStartMakespan)
# # ElectricPowerGragh(
# #     proposedElectricPowerResult, randomElectricPowerResult, preemptionElectricPowerResult, nodeStartElectricPowerResult
# # )
# EnergyConsumptionGragh(
#     proposedEnergyConsumption, randomEnergyConsumption, preemptionEnergyConsumption, nodeStartEnergyConsumption
# )
# deadlineRatioGragh(proposedDeadlineRatio, randomDeadlineRatio, preemptionDeadlineRatio, nodeStartDeadlineRatio)
