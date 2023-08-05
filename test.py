from scheduling import scheduling

from schedulingStrategy.NodeStartPriorityMetod import NodeStartPriorityAlgorithm
from schedulingStrategy.PreemptionPriorityMethod import PreemptionPriorityAlgorithm
from basicFunction.basicFunction import NormalJobPlacement
from environment.testEnvironment import test1_environment, test2_environment, test3_environment
from evaluation.gragh import MakeSpanGragh,ElectricPowerGragh
print("中断優先")
preemptionMakespan, preemptionElectricPowerResult = scheduling(
    "preemption", True, PreemptionPriorityAlgorithm, test3_environment
)
print("ノード起動優先")
nodeStartMakespan, nodeStartElectricPowerResult = scheduling(
    "nodeStart", True, NodeStartPriorityAlgorithm, test3_environment
)
print("通常ジョブのみ")
normalJobMakespan, normalJobElectricPowerResult = scheduling("normalJob", False, NormalJobPlacement, test3_environment)
# グラフ
MakeSpanGragh(normalJobMakespan, preemptionMakespan, nodeStartMakespan)
ElectricPowerGragh(normalJobElectricPowerResult, preemptionElectricPowerResult, nodeStartElectricPowerResult)
