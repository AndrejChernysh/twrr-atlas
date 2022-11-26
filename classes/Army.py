import random
import Convert
import Log
from classes.ArmyUnit import ArmyUnit
import singletons.Get as Get


class Army:

    _UIDPrefix = "AR"  # Must be unique across all classes!

    def __init__(self, faction, isledbynamedcharacter, starterUnitCount=None, armyunits=None):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Faction = faction
        self.isLedByNamedCharacter = bool(isledbynamedcharacter)
        self.ArmyUnits = Convert.List(armyunits)
        if self.isLedByNamedCharacter and len([u for u in self.ArmyUnits if u.Unit.NamedCharacterBodyguardLevel > 0]) == 0:
            unit = self.Faction.getNamedCharacterBodyguardUnit()
            Log.WarnIf(unit.IsGeneralUnitUpgrade, f"Added upgraded general unit as starter for {faction}")
            self.ArmyUnits.insert(0, ArmyUnit(unit))
        targetCount = Get.Setting("InitUnitsCountPerCity") if starterUnitCount is None else starterUnitCount
        while len(self.ArmyUnits) - 1 < targetCount:
            self.ArmyUnits.append(ArmyUnit(faction.getRandomStarterUnitLand()))
        assert len(self.ArmyUnits) <= 20, "Army %s has more than 20 units" % self

    def __str__(self):
        return "%s, %s" % (self.Faction, self.UID)

    def getArmyString(self):
        return "army\n%s" % "\n".join([u.getArmyUnitString() for u in self.ArmyUnits])
