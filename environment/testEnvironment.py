import os

current_path = os.getcwd()
print(current_path)

from environment.environmentClass import Environment
from environment.test.testSystem import testSystem
from environment.test.testJobSet import read_NormalJob,read_UrgentJob

test1_normalJob_queue = read_NormalJob("test1")
test2_normalJob_queue = read_NormalJob("test2")
test1_urgentJob_queue,test1_event = read_UrgentJob("test1")



test1_environment = Environment(testSystem, test1_normalJob_queue, test1_urgentJob_queue, test1_event)
test2_environment = Environment(testSystem, test2_normalJob_queue, test1_urgentJob_queue, test1_event)