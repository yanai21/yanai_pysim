import os

current_path = os.getcwd()
print(current_path)

from environment.environmentClass import Environment
from environment.test.testSystem import testSystem
from environment.test.testJobSet import normalJob_queue, urgentJob_queue, event

test1_environment = Environment(testSystem, normalJob_queue, urgentJob_queue, event)
