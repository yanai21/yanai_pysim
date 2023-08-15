import os

current_path = os.getcwd()
print(current_path)

from environment.environmentClass import Environment
from environment.test.testSystem import testSystem, aoba_testSystem_middle, aoba_testSystem
from environment.readJobSet import read_NormalJob, read_UrgentJob

test1_normalJob_queue = read_NormalJob("test", "test1")
test2_normalJob_queue = read_NormalJob("test", "test2")
test3_normalJob_queue = read_NormalJob("test", "test3")
test4_normalJob_queue = read_NormalJob("test", "test4")
test5_normalJob_queue = read_NormalJob("test", "test5")
test6_normalJob_queue = read_NormalJob("test", "test6")
tradeoff_normalJob_queue = read_NormalJob("test", "tradeoff")

test1_urgentJob_queue, test1_event = read_UrgentJob("test", "test1")
test2_urgentJob_queue, test2_event = read_UrgentJob("test", "test2")
test3_urgentJob_queue, test3_event = read_UrgentJob("test", "test3")
test4_urgentJob_queue, test4_event = read_UrgentJob("test", "test4")
test5_urgentJob_queue, test5_event = read_UrgentJob("test", "test5")
tradeoff_urgentJob_queue,tradeoff_event = read_UrgentJob("test", "tradeoff")

test1_environment = Environment(testSystem, test1_normalJob_queue, test1_urgentJob_queue, test1_event)
test2_environment = Environment(testSystem, test2_normalJob_queue, test1_urgentJob_queue, test1_event)
test3_environment = Environment(testSystem, test3_normalJob_queue, test1_urgentJob_queue, test1_event)
test4_environment = Environment(testSystem, test3_normalJob_queue, test2_urgentJob_queue, test2_event)
test5_environment = Environment(testSystem, test4_normalJob_queue, test3_urgentJob_queue, test3_event)
aoba_test1_environment = Environment(aoba_testSystem_middle, test5_normalJob_queue, test4_urgentJob_queue, test4_event)
aoba_test2_environment = Environment(aoba_testSystem, test6_normalJob_queue, test5_urgentJob_queue, test5_event)
aoba_tradeoff_environment = Environment(aoba_testSystem,tradeoff_normalJob_queue,tradeoff_urgentJob_queue,tradeoff_event)