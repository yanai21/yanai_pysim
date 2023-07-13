class Environment():
    def __init__(self,system,normalJob_queue,urgentJob_queue,event):
        self.system = system
        self.normalJob_queue = normalJob_queue
        self.urgentJob_queue = urgentJob_queue
        self.event = event
