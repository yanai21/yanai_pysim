import os

current_path = os.getcwd()
print(current_path)

from environment.environmentClass import Environment
from environment.deploy.system import aoba_a
from environment.deploy.jobSet import normalJob_queue,urgentJob_queue,event

deploy_environment = Environment(aoba_a, normalJob_queue, urgentJob_queue, event)

