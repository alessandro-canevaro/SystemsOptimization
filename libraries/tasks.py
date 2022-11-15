
class Event:
    def __init__(self, name, duration, period, deadline) -> None:
        self.name = name
        self.duration = duration
        self.period = period
        self.deadline = deadline

    def __repr__(self):
       return "{}: duration: {}, period: {}, deadline: {}".format(self.name, self.duration, self.period, self.deadline)
       
class TT(Event):
    def __init__(self, name, duration, period, deadline) -> None:
        super().__init__(name, duration, period, deadline)
    

class ET(Event):
    def __init__(self, name, duration, period, deadline, priority, separation) -> None:
        super().__init__(name, duration, period, deadline)
        self.priority = priority
        self.separation = separation

    def __repr__(self):
        return super().__repr__() + ", priority: {}".format(self.priority) + ", separation: {}".format(self.separation)

class PollingServer(Event):
    def __init__(self, name, duration, period, deadline, tasks, separation) -> None:
        super().__init__(name, duration, period, deadline)
        self.tasks = tasks
        self.separation = separation

    def __repr__(self):
        return super().__repr__() + ", separation: {}".format(self.separation) + ", num of tasks: {}".format(len(self.tasks))
