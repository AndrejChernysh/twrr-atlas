import random


class CharacterFemale:

    _UIDPrefix = "CF"  # Must be unique across all classes!

    def __init__(self, name, surname, age):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Name: str = name
        self.Surname: str = surname
        self.Age: int = age

    def __str__(self):
        return self.Name

    def getDescrStratEntry(self):
        return "character_record\t%s,\tfemale, command 0, influence 0, management 0, subterfuge 0, age %s, alive, never_a_leader" % (self.Name, self.Age)
