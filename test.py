from scheduling import scheduling

from schedulingStrategy.NodeStartPriorityMetod import NodeStartUrgentJobAssignment
# from schedulingStrategy.PreemptionPriorityMethod import PreemptionUrgentJobAssignment
from basicFunction.basicFunction import NormalJobPlacement
from environment.testEnvironment import test1_environment,test2_environment

# print("中断優先")
# preemptionMakespan,preemptionElectricPowerResult = scheduling("preemption",True,PreemptionUrgentJobAssignment,test1_environment)
print("ノード起動優先")
scheduling("nodeStart",True,NodeStartUrgentJobAssignment,test2_environment)
print("通常ジョブのみ")
scheduling("normalJob", False, NormalJobPlacement, test2_environment)
