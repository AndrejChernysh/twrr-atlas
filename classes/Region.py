import math

import Stringtools
import Convert
import classes.Position as Position
import classes.ResourcePosition as ResourcePosition
import classes.SettlementLevel as SettlementLevel
import random
import Log
import singletons.Get as Get


class Region:

    _UIDPrefix = "RE"  # Must be unique across all classes!

    def __init__(self, uid, nameregion, namecity, factionowner, population, factionnative, buildings, rebelfaction, rgb, fertility, iscapital, resourcepool: str, resourceslots: int, mercpool: str, distafrican: int, distarabic: int, distberber: int, distcaucasiandark: int, distberserker: int, distcaucasian: int, disteastasian: int, distegyptian: int, distmediterranean: int, distnorthafrican: int, distindian: int, hiddenresources):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(nameregion is None, f"Region {uid} has no NameRegion")
        Log.ErrorIf(namecity is None, f"Region {nameregion} has no NameCity")
        Log.ErrorIf(factionowner is None, f"Region {nameregion} has no FactionOwner")
        Log.ErrorIf(population is None, f"Region {nameregion} has no Population")
        Log.ErrorIf(factionnative is None, f"Region {nameregion} has no FactionNative")
        Log.ErrorIf(rebelfaction is None, f"Region {nameregion} has no RebelFaction")
        Log.ErrorIf(rgb is None, f"Region {nameregion} has no RGB")
        Log.ErrorIf(fertility is None, f"Region {nameregion} has no Fertility")
        Log.ErrorIf(iscapital is None, f"Region {nameregion} has no IsCapital")
        Log.ErrorIf(resourcepool is None, f"Region {nameregion} has no ResourcePool")
        Log.ErrorIf(resourceslots is None, f"Region {nameregion} has no ResourceSlots")
        Log.ErrorIf(mercpool is None, f"Region {nameregion} has no MercPoolId")
        Log.ErrorIf(distafrican is None, f"Region {nameregion} has no EDAfrican")
        Log.ErrorIf(distarabic is None, f"Region {nameregion} has no EDArabic")
        Log.ErrorIf(distberber is None, f"Region {nameregion} has no EDBerber")
        Log.ErrorIf(distcaucasiandark is None, f"Region {nameregion} has no EDCaucasianDark")
        Log.ErrorIf(distberserker is None, f"Region {nameregion} has no EDBerserker")
        Log.ErrorIf(distcaucasian is None, f"Region {nameregion} has no EDCaucasian")
        Log.ErrorIf(disteastasian is None, f"Region {nameregion} has no EDEastAsian")
        Log.ErrorIf(distegyptian is None, f"Region {nameregion} has no EDEgyptian")
        Log.ErrorIf(distmediterranean is None, f"Region {nameregion} has no EDMediterranean")
        Log.ErrorIf(distnorthafrican is None, f"Region {nameregion} has no EDNorthAfican")
        Log.ErrorIf(distindian is None, f"Region {nameregion} has no EDIndian")
        self.IdRegion = Convert.Str(nameregion.replace(" ", "_"))
        self.IdCity = Convert.Str(namecity.replace(" ", "_"))
        self.NameRegion = Convert.Str(nameregion)
        self.NameCity = Convert.Str(namecity)
        self.FactionOwner = Convert.Str(factionowner)
        self.FactionNative = Convert.Str(factionnative)
        Log.WarnIf(self.FactionNative == "slave", f"Region {self.IdRegion} has slave as FactionNative, must be non-slave")
        self.Population = Stringtools.intWithPossibleRange(population)
        self.Buildings = Stringtools.delimitedStringToList(buildings)
        self.RebelFaction = Convert.Str(rebelfaction)
        Log.ErrorIf(rgb is None, f"{self.IdRegion} has no RGB")
        self.R = int(rgb.split(" ")[0])
        self.G = int(rgb.split(" ")[1])
        self.B = int(rgb.split(" ")[2])
        self.Fertility = Stringtools.intWithPossibleRange(fertility)
        self.SettlementLevel = None
        self.NeighboringRegions = []
        self.IsCapital = bool(iscapital)
        self.PositionCity = None
        self.PositionPort = None
        self.PositionsAccessibleLand = []
        self.PositionsAccessibleLandOccupied = []
        self.PositionsResources: list[ResourcePosition.ResourcePosition] = []
        self.PositionsSea = []  # TODO
        self.StarterBuildingsCount = None
        self.ResourcePool: str = resourcepool
        self.ResourceSlots: int = Stringtools.intWithPossibleRange(resourceslots)
        EDSum = distafrican + distberber + distarabic + distcaucasiandark + distberserker + distcaucasian + disteastasian + distegyptian + distmediterranean + distnorthafrican + distindian
        Log.WarnIf(EDSum != 100, f"Sum of ethnic distributions in region {self.IdRegion} is {EDSum} and not 100")
        self.DistAfrican: int = distafrican
        self.DistArabic: int = distarabic
        self.DistBerber: int = distberber
        self.DistCaucasianDark: int = distcaucasiandark
        self.DistBerserker: int = distberserker
        self.DistCaucasian: int = distcaucasian
        self.DistEastAsian: int = disteastasian
        self.DistEgyptian: int = distegyptian
        self.DistMediterranean: int = distmediterranean
        self.DistNorthAfrican: int = distnorthafrican
        self.DistIndian: int = distindian
        self.MercPoolId: str = mercpool
        self.HiddenResources = Stringtools.delimitedStringToList(hiddenresources)

    def __str__(self):
        return self.NameRegion

    def __eq__(self, other):
        return self.IdRegion == other.IdRegion

    def addResource(self, resource):
        pos = random.choice(self.PositionsAccessibleLand)
        self.PositionsAccessibleLandOccupied.append(pos)
        self.PositionsResources.append(ResourcePosition.ResourcePosition(resource, pos))

    def getSettlementLevel(self) -> SettlementLevel:
        for settlementLevel in Get.AllSettlementLevels():
            if settlementLevel.MinPop <= self.Population <= settlementLevel.MaxPop:
                return settlementLevel

    def getCoreBuildingDescrStratEntry(self) -> str:
        if self.getSettlementLevel().Level == 0:
            return ""
        return [b for b in Get.AllBuildings() if self.getSettlementLevel().BuildingId == b.Id][0].toDescrStratBuildingEntry()

    def getDescrRegionsReligionDistribution(self) -> str:
        homeReligionId = Get.FactionById(self.FactionNative).Religion if self.FactionOwner == "slave" else Get.FactionById(self.FactionOwner).Religion
        homeReligionShare = random.randint(Get.Setting("HomeReligionInitialShareMin"), Get.Setting("HomeReligionInitialShareMax"))
        otherReligionsIds = [r.Id for r in Get.OtherReligionsSameGroupLike(homeReligionId)]
        remainingShare = 100 - homeReligionShare
        result = f"{homeReligionId} {homeReligionShare}"
        for otherReligion in otherReligionsIds:
            if not remainingShare == 0:
                if otherReligionsIds[-1] == otherReligion:
                    otherShare = remainingShare
                else:
                    otherShare = 1 if remainingShare == 1 else random.randint(1, remainingShare)
                    remainingShare -= otherShare
                result = f"{result} {otherReligion} {otherShare}"
        sum = 0
        for element in [e for e in result.split(" ") if e.isdigit()]:
            Log.WarnIf(element == "0", "One of beliefs in region %s has share 0!" % self.IdRegion)
            sum += int(element)
        Log.WarnIf(not sum == 100, "Sum of beliefs in region %s not 100!" % self.IdRegion)
        return result

    def getNonCoreBuildingDescrStratEntry(self) -> str:
        if self.getSettlementLevel().Level == 0 or len(self.Buildings) == 0:
            return ""
        return "\t".join([b.toDescrStratBuildingEntry() for b in Get.AllBuildings() if b.Id in self.Buildings])

    def getRandomPositionLand(self) -> Position:
        position = random.choice([p for p in self.PositionsAccessibleLand if p.UID not in self.PositionsAccessibleLandOccupied])
        self.PositionsAccessibleLandOccupied.append(position.UID)
        return position

    def getAddableBuildings(self):
        chainsAlreadyHere = [Get.BuildingById(b).BuildingChain for b in self.Buildings]
        bldngs = [b for b in Get.AllBuildings() if b not in self.Buildings and b.Level <= self.SettlementLevel.Level
                  and b.BuildingChain not in chainsAlreadyHere and Get.BuildingChainById(b.BuildingChain).IsStarter
                  and not Get.BuildingChainById(b.BuildingChain).RequiresCoast]
        bldngsCoast = [b for b in Get.AllBuildings() if b not in self.Buildings and b.Level <= self.SettlementLevel.Level
                       and b.BuildingChain not in chainsAlreadyHere and Get.BuildingChainById(b.BuildingChain).IsStarter
                       and Get.BuildingChainById(b.BuildingChain).RequiresCoast]
        if self.PositionPort is not None:
            return bldngs + bldngsCoast
        return bldngs

    def getPositionsResourcesByResourceId(self, resourceId):
        return [r for r in self.PositionsResources if r.Resource.Id == resourceId]

    def getPositionsResourcesOnMap(self):
        return [r for r in self.PositionsResources if r.Resource.IsOnMap]

    def getAllResourceIdsAsCommaSeparatedString(self):
        return ", ".join(list(set([r.Resource.Id for r in self.PositionsResources])))

    def getAllHiddenResourceIdsAsCommaSeparatedString(self):
        hiddenResources = list(set([r for r in self.HiddenResources]))
        if len(hiddenResources) > 0:
            return ", ".join(hiddenResources)
        return "none"

    def scriptFireInCity(self):
        return f"console_command event fire {self.PositionCity.X}, {self.PositionCity.Y}"

    def scriptEarthquakeInCity(self):
        return f"console_command event earthquake {self.PositionCity.X}, {self.PositionCity.Y}"

    def scriptFloodInCity(self):  # Do not use in Region multiple times because each time you generate a message
        return f"console_command event flood {self.PositionCity.X}, {self.PositionCity.Y}"

    def scriptPlagueInCity(self):
        return f"console_command event plague {self.PositionCity.X}, {self.PositionCity.Y}"

    def scriptRevoltInCity(self):
        return f"provoke_rebellion {self.IdCity}"

    def scriptFireInPort(self):
        return f"console_command event fire {self.PositionPort.X}, {self.PositionPort.Y}"

    def scriptFireInRegion(self):
        code = []
        for position in random.sample(self.PositionsAccessibleLand, 4):
            code.append(f"console_command event fire {position.X}, {position.Y}")
        return "\n\t".join(code)
