
import Enums
import Log
import Stringtools
import Translatetools
import Convert
import singletons.Get as Get
from classes.Faction import Faction


class Unit:

    _UIDPrefix = "UN"  # Must be unique across all classes!

    def __init__(self, uid, id, dictionary, name, category, myclass, voicetype, soldier, spec, numbersoldiers, numberextras, collisionmass, mount, attributes, formation, hp, hpextras, statpri, statpriattr, statsec, statsecattr, statpriarmour, statsecarmour, statheat, statground, morale, discipline, training, statchargedist, turns, costrecruit, costupkeep, costupgradeweapons, costupgradearmour, ownership, buildingchainLvl, descr):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(id is None, f"Unit {uid} has no ID")
        Log.ErrorIf(dictionary is None, f"Unit {id} has no Dictionary")
        Log.ErrorIf(name is None, f"Unit {id} has no Name")
        Log.ErrorIf(category is None, f"Unit {id} has no Category")
        Log.ErrorIf(myclass is None, f"Unit {id} has no Class")
        Log.ErrorIf(voicetype is None, f"Unit {id} has no VoiceType")
        Log.ErrorIf(soldier is None, f"Unit {id} has no Soldier")
        Log.ErrorIf(numbersoldiers is None, f"Unit {id} has no Soldiers")
        Log.ErrorIf(numberextras is None, f"Unit {id} has no Extras")
        Log.ErrorIf(collisionmass is None, f"Unit {id} has no Mass")
        Log.ErrorIf(formation is None, f"Unit {id} has no Formation")
        Log.ErrorIf(hp is None, f"Unit {id} has no HP")
        Log.ErrorIf(hpextras is None, f"Unit {id} has no HPExtras")
        Log.ErrorIf(statpri is None, f"Unit {id} has no StatPri")
        Log.ErrorIf(statpriattr is None, f"Unit {id} has no StatPriAttr")
        Log.ErrorIf(statsec is None, f"Unit {id} has no StatSec")
        Log.ErrorIf(statsecattr is None, f"Unit {id} has no StatSecAttr")
        Log.ErrorIf(statpriarmour is None, f"Unit {id} has no StatPriArmour")
        Log.ErrorIf(statsecarmour is None, f"Unit {id} has no StatSecArmour")
        Log.ErrorIf(statheat is None, f"Unit {id} has no StatHeat")
        Log.ErrorIf(statground is None, f"Unit {id} has no StatGround")
        Log.ErrorIf(morale is None, f"Unit {id} has no Morale")
        Log.ErrorIf(discipline is None, f"Unit {id} has no Discipline")
        Log.ErrorIf(training is None, f"Unit {id} has no Training")
        Log.ErrorIf(statchargedist is None, f"Unit {id} has no ChargeDist")
        Log.ErrorIf(costrecruit is None, f"Unit {id} has no CostRecr")
        Log.ErrorIf(costupkeep is None, f"Unit {id} has no CostUpk")
        Log.ErrorIf(costupgradeweapons is None, f"Unit {id} has no CostUpgrWpn")
        Log.ErrorIf(costupgradearmour is None, f"Unit {id} has no CostUpgrArm")
        Log.ErrorIf(ownership is None, f"Unit {id} has no Ownership")
        self.Id = Convert.Str(id)
        self.Dictionary = Convert.Str(dictionary)
        Log.ErrorIf(" " in dictionary, f"Unit dictionary {dictionary} contains whitespaces which is not allowed")
        self.Name = Convert.Str(name)
        self.Category = Convert.Str(category)
        assert self.Category in Enums.UNIT_CATEGORIES, "%s category %s <> %s" % (self.Id, self.Category, Enums.UNIT_CATEGORIES)
        self.Class = Convert.Str(myclass)
        assert self.Class in Enums.UNIT_CLASSES, "%s class %s <> %s" % (self.Id, self.Class, Enums.UNIT_CLASSES)
        self.VoiceType = Convert.Str(voicetype)
        self.Soldier = Convert.Str(soldier)
        Log.ErrorIf(spec is not None and not str(spec).count(":") == 1, f"{self.Dictionary} special format not type:reference (but {spec})")
        Log.ErrorIf(spec is not None and spec.split(":")[0] not in Enums.UNIT_SPECIALS, f"{self} special type invalid")
        self.Special = Convert.Str(spec)
        self.Ship = None if spec is None or spec.split(":")[0].lower() != "ship" else spec.split(":")[1]
        Log.WarnIf(self.Category == "ship" and self.Ship is None, f"{self} is category ship without Ship")
        Log.WarnIf(not self.Category == "ship" and self.Ship is not None, f"{self} has Ship but is not category ship")
        self.Animal = None if spec is None or spec.split(":")[0].lower() != "animal" else spec.split(":")[1]
        Log.WarnIf(self.Category == "handler" and self.Animal is None, f"{self} is category handler without Animal")
        Log.WarnIf(not self.Category == "handler" and self.Animal is not None, f"{self} has Animal but is not category handler")
        self.Engine = None if spec is None or spec.split(":")[0].lower() != "engine" else spec.split(":")[1]
        Log.WarnIf(self.Category == "siege" and self.Engine is None, f"{self} is category siege without Engine")
        Log.WarnIf(not self.Category == "siege" and self.Engine is not None, f"{self} has Engine but is not category siege")
        self.NumberSoldiers = Convert.Int(numbersoldiers)
        self.NumberExtras = Convert.Int(numberextras)
        self.CollisionMass = collisionmass
        self.Mount = Convert.Str(mount)
        self.Attributes = Stringtools.delimitedStringToList(attributes)
        for attribute in Stringtools.delimitedStringToList(Get.Setting("AttributesAllUnits")):
            self.Attributes.append(attribute)
        for i, a in enumerate(self.Attributes):
            Log.WarnIfNot(a in Enums.UNIT_ATTRIBUTES, f"Unit {self.Id} has invalid attribute {a}")
            if "general_unit" in self.Attributes and a == "can_horde":
                self.Attributes.pop(i)
        self.Formation = Convert.Str(formation)
        self.HP = Convert.Int(hp)
        self.HPExtras = Convert.Int(hpextras)
        self.StatPri = Convert.Str(statpri)
        self.StatPriAttr = Convert.Str(statpriattr)
        self.StatSec = Convert.Str(statsec)
        self.StatSecAttr = Convert.Str(statsecattr)
        self.StatPriArmour = Convert.Str(statpriarmour)
        self.StatSecArmour = Convert.Str(statsecarmour)
        self.StatHeat = Convert.Int(statheat)
        self.StatGround = Convert.Str(statground)
        self.Morale = Convert.Int(morale)
        self.Discipline = Convert.Str(discipline)
        assert self.Discipline in Enums.UNIT_DISCIPLINES, "%s discipline %s <> %s" % (self.Id, self.Discipline, Enums.UNIT_DISCIPLINES)
        self.Training = Convert.Str(training)
        assert self.Training in Enums.UNIT_TRAINING, "%s training %s <> %s" % (self.Id, self.Training, Enums.UNIT_TRAINING)
        self.StatChargeDist = Convert.Int(statchargedist)
        self.Turns = Convert.Int(turns)
        self.IsMercenary = "mercenary_unit" in self.Attributes
        self.CostRecruit = Convert.Int(costrecruit) * Get.Setting("MercCostMultiplier") if self.IsMercenary else Convert.Int(costrecruit)
        self.CostUpkeep = Convert.Int(costupkeep)
        self.CostUpgradeWeapons = Convert.Int(costupgradeweapons)
        self.CostUpgradeArmour = Convert.Int(costupgradearmour)
        self.Ownership = Translatetools.factionOrCultureListTranslateToFactionList(ownership)
        shadowFactions = []
        for factionId in self.Ownership:
            if Get.FactionById(factionId).IsPlayable:
                shadowFactions.append(f"{factionId}_s")
        self.Ownership += shadowFactions
        Log.ErrorIf(ownership is None, f"Unit {id} has no ownership factions")
        self.BuildingChain = None if buildingchainLvl is None else buildingchainLvl.split(":")[0]
        self.BuildingChainLvl = None if buildingchainLvl is None else int(buildingchainLvl.split(":")[1])
        self.IsGeneralUnitUpgrade = "general_unit_upgrade" in " ".join(self.Attributes)
        self.NamedCharacterBodyguardLevel = 0
        if "general_unit" in self.Attributes and not self.IsGeneralUnitUpgrade:
            self.NamedCharacterBodyguardLevel = 1
        elif "general_unit" in self.Attributes and self.IsGeneralUnitUpgrade:
            self.NamedCharacterBodyguardLevel = 2
        starterUnitsChains = Stringtools.delimitedStringToList(Get.Setting("BuildingChainsStarterUnits"))
        self.IsStarter = False if buildingchainLvl is None else buildingchainLvl in starterUnitsChains
        self.Descr = "TODO" if descr is None else descr
        self.DescrShort = "TODO" if descr is None else "%s." % descr.split(".")[0]
        self.IsFemale: bool = "women" in self.Id or "maidens" in self.Id or "amazon" in self.Id

    def __str__(self):
        return self.Name

    def __eq__(self, other):
        return self.Id == other.Id

    def GetIsFemaleOrEmpty(self):
        return "is_female" if self.IsFemale else ""

    def GetOwnershipFactions(self) -> list[Faction]:
        result = []
        for faction in self.Ownership:
            result.append(Get.FactionById(faction))
        return result

    def GetAttributesAsCommaDelimitedString(self):
        return ", ".join(self.Attributes)

    def GetOwnershipAsCommaDelimitedString(self):
        return ", ".join(self.Ownership)

    def GetExportDescrUnitMountEntries(self):
        if self.Mount is not None:
            mount = Get.MountById(self.Mount)
            return "\nmount            %s\nmount_effect     %s" % (mount.Id, mount.Effect)
        return ""

    def GetExportDescrUnitEngineEntry(self):
        if self.Engine is not None:
            return f"\nengine           {self.Engine}"
        return ""

    def GetExportDescrUnitAnimalEntry(self):
        if self.Animal is not None:
            return f"\nanimal           {self.Animal}"
        return ""

    def GetExportDescrUnitShipEntry(self):
        if self.Ship is not None:
            return f"\nship           {self.Ship}"
        return ""

    def GetRequiredStringNoBonus(self):
        if self.Ownership == "all":
            return ""
        factionIdsWithBonusForThisUnit = []
        for factionId in self.Ownership:
            faction = Get.FactionById(factionId)
            if len(faction.BonusBuildingEffects) > 0:
                for bonusBuildingEffect in faction.BonusBuildingEffects:
                    if self.BuildingChain in bonusBuildingEffect and "fbonus" in bonusBuildingEffect:
                        factionIdsWithBonusForThisUnit.append(factionId)
        factionIdsNoBonus = list(set(self.Ownership) - set(factionIdsWithBonusForThisUnit))
        factionIdsNoBonusCommaSeparatedList = ", ".join(factionIdsNoBonus)
        return f"requires factions {{ {factionIdsNoBonusCommaSeparatedList}, }}"

    def GetRequiredStringWithBonus(self):
        if self.Ownership == "all":
            return ""
        factionIdsWithBonusForThisUnit = []
        for factionId in self.Ownership:
            faction = Get.FactionById(factionId)
            if len(faction.BonusBuildingEffects) > 0:
                for bonusBuildingEffect in faction.BonusBuildingEffects:
                    if self.BuildingChain in bonusBuildingEffect and "fbonus" in bonusBuildingEffect:
                        factionIdsWithBonusForThisUnit.append(factionId)
        factionIdsWithBonusCommaSeparatedList = ", ".join(factionIdsWithBonusForThisUnit)
        return f"requires factions {{ {factionIdsWithBonusCommaSeparatedList}, }}"
