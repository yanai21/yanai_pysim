import os

current_path = os.getcwd()
print(current_path)

from environment.environmentClass import Environment
from environment.test.testSystem import testSystem,aoba_testSysytem
from environment.test.testJobSet import read_NormalJob,read_UrgentJob

test1_normalJob_queue = read_NormalJob("test1")
test2_normalJob_queue = read_NormalJob("test2")
test3_normalJob_queue = read_NormalJob("test3")
test4_normalJob_queue = read_NormalJob("test4")
test5_normalJob_queue = read_NormalJob("test5")

test1_urgentJob_queue,test1_event = read_UrgentJob("test1")
test2_urgentJob_queue,test2_event = read_UrgentJob("test2")
test3_urgentJob_queue,test3_event = read_UrgentJob("test3")
test4_urgentJob_queue,test4_event = read_UrgentJob("test4")

test1_environment = Environment(testSystem, test1_normalJob_queue, test1_urgentJob_queue, test1_event)
test2_environment = Environment(testSystem, test2_normalJob_queue, test1_urgentJob_queue, test1_event)
test3_environment = Environment(testSystem, test3_normalJob_queue, test1_urgentJob_queue, test1_event)
test4_environment = Environment(testSystem, test3_normalJob_queue, test2_urgentJob_queue, test2_event)
test5_environment = Environment(testSystem, test4_normalJob_queue, test3_urgentJob_queue, test3_event)
aoba_test1_environment = Environment(aoba_testSysytem, test5_normalJob_queue, test4_urgentJob_queue, test4_event)