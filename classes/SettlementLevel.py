import Convert


class SettlementLevel:

    _UIDPrefix = "SL"  # Must be unique across all classes!

    def __init__(self, uid, id, level, name, building, minpop, maxpop, rebelunitcount, rebelunitexp, rebelunitarmourlvl, rebelunitweaponlvl, buildingid, starterbuildingscount):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        self.Id = Convert.Str(id)
        self.Level = Convert.Int(level)
        self.Name = Convert.Str(name)
        self.Building = Convert.Str(building)
        self.MinPop = Convert.Int(minpop)
        self.MaxPop = Convert.Int(maxpop)
        self.RebelUnitCount = Convert.Str(rebelunitcount)
        self.RebelUnitExp = Convert.Str(rebelunitexp)
        self.RebelUnitArmourLvl = Convert.Str(rebelunitarmourlvl)
        self.RebelUnitWeaponLvl = Convert.Str(rebelunitweaponlvl)
        self.BuildingId = Convert.Str(buildingid)
        self.StarterBuildingsCount = Convert.Str(starterbuildingscount)

    def __str__(self):
        return self.Name
