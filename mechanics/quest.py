# quest.py:

class Quest:
    def __init__(self, name, description, conditions):
        self.name = name # string
        self.description = description # string
        self.conditions = conditions # dictionary
        self.progress = dict.fromkeys(self.conditions.keys(), 0)
        
    def check(self, item):
        if item in self.conditions:
            self.conditions[item] += 1
