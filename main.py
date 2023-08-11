from scheduling import scheduling

from schedulingStrategy.NodeStartPriorityMetod import NodeStartPriorityAlgorithm
from schedulingStrategy.PreemptionPriorityMethod import PreemptionPriorityAlgorithm
from basicFunction.basicFunction import NormalJobPlacement

# データ管理
from environment.deployEnvironment import deploy_environment
from evaluation.gragh import MakeSpanGragh, ElectricPowerGragh

environment = deploy_environment
print(environment.system)
print("中断優先")
preemptionMakespan, preemptionElectricPowerResult = scheduling(
    "preemption", True, PreemptionPriorityAlgorithm, environment
)
print("ノード起動優先")
nodeStartMakespan, nodeStartElectricPowerResult = scheduling("nodeStart", True, NodeStartPriorityAlgorithm, environment)
print("通常ジョブのみ")
normalJobMakespan, normalJobElectricPowerResult = scheduling("normalJob", False, NormalJobPlacement, environment)
# グラフ
MakeSpanGragh(normalJobMakespan, preemptionMakespan, nodeStartMakespan)
ElectricPowerGragh(normalJobElectricPowerResult, preemptionElectricPowerResult, nodeStartElectricPowerResult)
