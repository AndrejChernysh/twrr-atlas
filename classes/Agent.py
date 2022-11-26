import random
import Enums


class Agent:

    _UIDPrefix = "AG"  # Must be unique across all classes!

    def __init__(self, name, surname, agentType, position):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Name = str(name)
        self.Surname = str(surname)
        self.agentType = str(agentType)
        assert self.agentType in Enums.AGENTS, "Invalid agent type for %s: %s" % (self.agentType, self)
        self.Position = position
        self.Age = random.randint(20, 50)

    def __str__(self):
        return "%s %s" % (self.Name, self.Surname)

    def getDescrStratString(self):
        fullname = "%s %s" % (self.Name, self.Surname)
        return "character\t%s, %s, age %s, , x %s, y %s\n\n" % (fullname, self.agentType, self.Age, self.Position.X, self.Position.Y)
