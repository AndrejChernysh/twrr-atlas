import random
import Convert
import classes.Army as Army
import classes.Faction as Faction
import classes.Position as Position
import singletons.Get as Get


class General:

    _UIDPrefix = "GN"  # Must be unique across all classes!

    def __init__(self, name: str, position: Position, army: Army, faction: Faction, subfaction: Faction):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Name = Convert.Str(name)
        assert self.Name in [n.Id for n in Get.AllNames() if n.Type == "characters" and (n.Culture == faction.Culture or (faction.IsSlave and n.Culture == subfaction.Culture))], "Name %s invalid for %s" % (self.Name, faction)
        self.Age = 20
        self.Position = position
        self.Army = army
        self.Faction = faction
        self.SubFaction = subfaction

    def __str__(self):
        return self.Name

    def getDescrStratEntry(self) -> str:
        subfaction = "sub_faction %s," % self.SubFaction.Id if self.Faction.IsSlave else ""
        return "character\t%s %s, general, age %s, , x %s, y %s\n%s" % (subfaction, self, self.Age, self.Position.X, self.Position.Y, self.Army.getArmyString())
