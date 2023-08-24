import os

current_path = os.getcwd()
print(current_path)

from environment.environmentClass import Environment
from environment.test.testSystem import testSystem, aoba_testSystem_middle, aoba_testSystem
from environment.readJobSet import read_NormalJob, read_UrgentJob

test1_environment = Environment(testSystem, "test", "test1", "test1")
