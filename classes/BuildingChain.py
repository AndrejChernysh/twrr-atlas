import Enums
import Convert
import Log
import Translatetools
import singletons.Get as Get


class BuildingChain:

    _UIDPrefix = "BC"  # Must be unique across all classes!

    def __init__(self, uid, id, name, baserounds, basemoney, isstarter, icon, ownership, exclusivetag, aionly, classification: str, recruitnewuniteachlvl: bool, reqcoast: bool, reqresource):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(id is None, f"BuildingChain {uid} has no ID")
        Log.ErrorIf(name is None, f"BuildingChain {id} has no Name")
        Log.ErrorIf(baserounds is None, f"BuildingChain {id} has no BaseRounds")
        Log.ErrorIf(basemoney is None, f"BuildingChain {id} has no BaseMoney")
        Log.ErrorIf(isstarter is None, f"BuildingChain {id} has no IsStarter")
        Log.ErrorIf(icon is None, f"BuildingChain {id} has no Icon")
        Log.ErrorIf(ownership is None, f"BuildingChain {id} has no Ownership")
        Log.ErrorIf(aionly is None, f"BuildingChain {id} has no AIOnly")
        Log.ErrorIf(classification is None, f"BuildingChain {id} has no Class")
        Log.ErrorIf(recruitnewuniteachlvl is None, f"BuildingChain {id} has no RecruitNewUnitEachLvl")
        Log.ErrorIf(reqcoast is None, f"BuildingChain {id} has no NeedsCoast")
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.BaseRounds = Convert.Int(baserounds)
        Log.ErrorIf(self.BaseRounds == 0, f"BuildingChain {id} has base rounds 0 - will never be completed!")
        self.BaseMoney = Convert.Int(basemoney)
        self.IsStarter = bool(isstarter)
        self.Icon = Convert.Str(icon)
        assert self.Icon in Enums.BUILDINGCHAINS_ICONS, "%s icon %s <> %s" % (self.Id, self.Icon, Enums.BUILDINGCHAINS_ICONS)
        self.Ownership = Translatetools.factionOrCultureListTranslateToFactionList(ownership)
        shadowFactions = []
        for factionId in self.Ownership:
            if Get.FactionById(factionId).IsPlayable:
                shadowFactions.append(f"{factionId}_s")
        self.Ownership += shadowFactions
        self.ExclusiveTag = Convert.Str(exclusivetag)
        self.AiOnly = bool(aionly)
        self.Classification: str = classification
        self.RecruitNewUnitEachLvl: bool = recruitnewuniteachlvl
        Log.WarnIf(classification not in Enums.BUILDINGCHAINS_CLASSES, f"{self} has invalid classification {classification}")
        self.RequiresCoast = reqcoast
        self.PlayerOnly = False
        self.IsConstructable = True
        self.RequiresResources = Convert.ListFromCommaDelimitedString(reqresource)
        Log.WarnIf(classification == "core" and self.Id != "core_building", f"{self} has classification {classification} but is not core_buildings, will not show up picture in building browser")

    def __str__(self):
        return self.Id

    def __eq__(self, other):
        return self.Id == other.Id

    def getLevelsBuilding(self):
        return [b for b in sorted(Get.BuildingsByBuildingChainId(self.Id), key=lambda x: x.Level)]

    def getLevelsBuildingIdString(self, separator):
        return separator.join([b.Id for b in sorted(Get.BuildingsByBuildingChainId(self.Id), key=lambda x: x.Level)])

    def getPossibleExclusiveTag(self):
        if self.ExclusiveTag is None:
            return ""
        return "tag %s" % self.ExclusiveTag

    def getLowestLevel(self):
        return min([b.Level for b in Get.AllBuildings() if b.BuildingChain == self.Id])