import random
import singletons.Get as Get


class ArmyUnit:

    _UIDPrefix = "AU"  # Must be unique across all classes!

    def __init__(self, unit, exp=None, armourlvl=None, weaponlvl=None):
        self.UID = "%s%s" % (self._UIDPrefix, random.randint(0, 9999999999999999))
        self.Unit = unit
        self.Exp = exp
        if self.Exp is None:
            self.Exp = random.randint(Get.Setting("InitUnitsExpMin"), Get.Setting("InitUnitsExpMax"))
        assert 0 <= self.Exp <= 9, "ArmyUnit %s Exp %s (must be 0-9)" % self
        self.ArmourLvl = armourlvl
        if self.ArmourLvl is None:
            self.ArmourLvl = random.randint(Get.Setting("InitUnitsArmourLvlMin"), Get.Setting("InitUnitsArmourLvlMax"))
        assert 0 <= self.ArmourLvl <= 3, "ArmyUnit %s ArmourLvl %s (must be 0-3)" % self
        self.WeaponLvl = weaponlvl
        if self.WeaponLvl is None:
            self.WeaponLvl = random.randint(Get.Setting("InitUnitsWpnLvlMin"), Get.Setting("InitUnitsWpnLvlMax"))
        assert 0 <= self.WeaponLvl <= 3, "ArmyUnit %s WeaponLvl %s (must be 0-3)" % self

    def __str__(self):
        return "%s, %s" % (self.Unit, self.UID)

    def getArmyUnitString(self):
        return "unit\t%s\texp %s armour %s weapon_lvl %s" % (self.Unit.Id, self.Exp, self.ArmourLvl, self.WeaponLvl)
