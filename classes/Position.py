import random
import Convert


class Position:

    _UIDPrefix = "PO"  # Must be unique across all classes!

    def __init__(self, x, y):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.X = Convert.Int(x)
        self.Y = Convert.Int(y)

    def __str__(self):
        return "%s, %s" % (self.X, self.Y)

    def __eq__(self, other):
        return self.X * 10000 + self.Y == other.X * 10000 + other.Y
