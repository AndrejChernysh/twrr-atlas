import random
import Convert
import Log
import Stringtools
import classes.Army as Army
import classes.Faction as Faction
import classes.Position as Position
import singletons.Get as Get


class Character:

    _UIDPrefix = "CH"  # Must be unique across all classes!

    def __init__(self, name: str, surname: str, isleader: bool, isheir: bool, age, position: Position, army: Army, faction: Faction, subfaction: Faction):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Name = Convert.Str(name)
        Log.ErrorIf(self.Name not in [n.Id for n in Get.AllNames() if n.Type == "characters" and (n.Culture == faction.Culture or (faction.IsSlave and n.Culture == subfaction.Culture))], f"Name {self.Name} invalid for {faction}")
        self.Surname = Convert.Str(surname)
        Log.ErrorIf(self.Surname is not None and self.Surname not in [n.Id for n in Get.AllNames() if n.Type == "surname" and (n.Culture == faction.Culture or (faction.IsSlave and n.Culture == subfaction.Culture))], f"Name {self.Name} invalid for {faction}")
        Log.ErrorIf(isleader and isheir, f"Character {self} cannot be leader and heir simultaneously")
        self.IsLeader = bool(isleader)
        self.IsHeir = bool(isheir)
        self.Age = Convert.Int(age)
        Log.ErrorIf(self.Age < 17, f"Character {self} ({faction}) must be at least 17 years old but is {self.Age}")
        self.Position = position
        self.Army = army
        self.Faction = faction
        self.SubFaction = subfaction

    def __str__(self):
        return self.Name if self.Surname is None else "%s %s" % (self.Name, self.Surname)

    def getDescrStratEntry(self) -> str:
        rank = ", leader" if self.IsLeader else ""
        rank = ", heir" if self.IsHeir else rank
        subfaction = "sub_faction %s," % self.SubFaction.Id if self.Faction.IsSlave else ""
        return "character\t%s %s, named character%s, age %s, , x %s, y %s\n%s\n%s" % (subfaction, self, rank, self.Age, self.Position.X, self.Position.Y, self.getDescrStratTraits(rank), self.Army.getArmyString())

    def getDescrStratTraits(self, rank) -> str:
        if self.Faction.IsSlave:
            rank = random.choice([", leader", " , heir"])
        traits = ["LoyaltyStarter 1"]  # Needed to have shadow factions
        traits.append(f"{self.SubFaction.Religion} 1") if self.Faction.IsSlave else traits.append(f"{self.Faction.Religion} 1")
        if not rank == "":
            settingNames = [s for s in Get.AllSettingNames() if "Trait" in s and "Name" in s and rank.split(" ")[1] in s.lower()]
            for settingName in settingNames:
                value = Stringtools.intWithPossibleRange(Get.Setting(settingName.replace("Name", "Value")))
                if value > 0:
                    traits.append("%s %s" % (Get.Setting(settingName), value))
            if len(traits) == 0:
                return ""
        return "traits " + ", ".join(traits)
