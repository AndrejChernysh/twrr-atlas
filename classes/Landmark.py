from classes.Position import Position


class Landmark:

    _UIDPrefix = "LM"  # Must be unique across all classes!

    def __init__(self, uid, id, positionX, positionY, name):
        self.UID = uid
        self.Id = id
        self.Position = Position(positionX, positionY)
        self.Name = name

    def __str__(self):
        return self.Id
