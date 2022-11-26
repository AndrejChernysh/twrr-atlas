import random
import statistics
from pathlib import Path
import Enums
import Globals
import OStools
import Stringtools
from classes.Agent import Agent
from classes.Army import Army
from classes.ArmyUnit import ArmyUnit
from classes.General import General
from classes.Character import Character
from classes.Message import Message
from classes.Culture import Culture
from classes.CharacterFemale import CharacterFemale
from classes.Name import Name
from classes.Region import Region
from classes.Position import Position
from classes.Faction import Faction
from classes.BuildingChain import BuildingChain
from classes.Building import Building
from classes.Resource import Resource
from classes.MercPool import MercPool
import singletons.Get as Get
import Log


class World(object):
    Factions: list[Faction] = []
    ShadowFactions: list[Faction] = []
    Cultures: list[Culture] = []
    Religions = []
    Units = []
    Names = []
    BuildingChains: list[BuildingChain] = []
    Buildings: list[Building] = []
    Resources: list[Resource] = []
    ResourceCounts = dict()
    SettlementLevels = []
    RebelFactions = []
    Regions: list[Region] = []
    Mounts = []
    Landmarks = []
    MercPools: list[MercPool] = []
    Messages: list[Message] = []

    @classmethod
    def loadFactions(cls, factions):
        cls.Factions = factions
        Log.Info("Initialized %s factions" % len(cls.Factions))

    @classmethod
    def loadCultures(cls, cultures):
        cls.Cultures = cultures
        Log.Info("Initialized %s cultures" % len(cls.Cultures))

    @classmethod
    def loadReligions(cls, religions):
        cls.Religions = religions
        Log.Info("Initialized %s religions" % len(cls.Religions))

    @classmethod
    def loadUnits(cls, units):
        cls.Units = units
        Log.Info("Initialized %s units" % len(cls.Units))

    @classmethod
    def loadMercPools(cls, mercpools):
        cls.MercPools = mercpools
        Log.Info("Initialized %s mercpools" % len(cls.MercPools))

    @classmethod
    def loadNames(cls, names):
        cls.Names = names
        Log.Info("Initialized %s names" % len(cls.Names))

    @classmethod
    def loadBuildingChains(cls, buildingchains):
        cls.BuildingChains = buildingchains
        Log.Info("Initialized %s buildingchains" % len(cls.BuildingChains))

    @classmethod
    def loadBuildings(cls, buildings):
        cls.Buildings = buildings
        Log.Info("Initialized %s buildings" % len(cls.Buildings))

    @classmethod
    def loadLandmarks(cls, landmarks):
        cls.Landmarks = landmarks
        Log.Info("Initialized %s landmarks" % len(cls.Landmarks))

    @classmethod
    def loadResources(cls, resources):
        cls.Resources = resources
        Log.Info("Initialized %s resources" % len(cls.Resources))

    @classmethod
    def loadSettlementLevels(cls, settlementlevels):
        cls.SettlementLevels = settlementlevels
        Log.Info("Initialized %s settlementlevels" % len(cls.SettlementLevels))

    @classmethod
    def loadRebelFactions(cls, rebelfactions):
        cls.RebelFactions = rebelfactions
        Log.Info("Initialized %s rebelfactions" % len(cls.RebelFactions))

    @classmethod
    def loadRegions(cls, regions):
        cls.Regions = regions
        Log.Info("Initialized %s regions" % len(cls.Regions))

    @classmethod
    def loadMounts(cls, mounts):
        cls.Mounts = mounts
        Log.Info("Initialized %s mounts" % len(cls.Mounts))

    @classmethod
    def checkLoad(cls):
        Log.Info("Running Checks")
        for originalFaction in Enums.ORIGINAL_FACTIONIDS:
            Log.ErrorIf(originalFaction not in Get.AllFactionIds(), f"Faction {originalFaction} not in Configuration.xlsx - game will crash, do not remove any original faction id!")
        for faction in cls.Factions:
            countUnits = len([u for u in cls.Units if faction.Id in u.Ownership])
            Log.WarnIf(countUnits == 0, "Faction %s has no unit(s)" % faction)
            countCapitals = len([r for r in cls.Regions if faction.Id == r.FactionOwner and r.IsCapital])
            Log.ErrorIf(countCapitals > 1, f"{faction} has {countCapitals} capitals instead of 0 or 1")
            if len(faction.BonusBuildingEffects) > 0:
                for bbe in faction.BonusBuildingEffects:
                    chain, effect = bbe.split(":")
                    Log.ErrorIfNot(chain in [c.Id for c in Get.AllBuildingChains()], f"{faction.Id} BonusBuildingEffect invalid chain {chain}")
        pools = Get.AllResourcePools()
        regions = Get.AllRegions()
        mercpools = Get.AllMercPoolIds()
        for mercpool in mercpools:
            regionCount = len([r for r in regions if r.MercPoolId == mercpool])
            Log.WarnIf(regionCount < 1, f"MercPool {mercpool} has no regions")
        for resourcepool in pools:
            regionCount = len([r for r in regions if r.ResourcePool == resourcepool])
            Log.WarnIf(regionCount < 1, f"Resource pool {resourcepool} has no regions")
        for region in regions:
            Log.WarnIf(region.ResourcePool not in pools, "Region %s has resource pool %s which is not in Resources" % (region, region.ResourcePool))
            Log.WarnIf(region.ResourcePool not in pools, f"Region {region}: resource pool {region.ResourcePool} not in Resources")
            Log.WarnIf(region.MercPoolId not in mercpools, f"Region {region}: merc pool {region.MercPoolId} not in MercPools")
        for chain in Get.AllBuildingChains():
            if len(chain.RequiresResources) > 0:
                for r in chain.RequiresResources:
                    validResources = [r.Id for r in Get.AllResources()]
                    Log.ErrorIf(r not in validResources, f"{chain} invalid resource requirement: {r}")

    @classmethod
    def init(cls):
        cls.Resources.append(Resource(999, "nobuild", None, None, "hidden", None, None, None, None, None, None, None, None, None, False, None, None, None, "Desert"))
        deadFactions = 0
        for i, faction in enumerate(cls.Factions):
            if len(faction.getStartingRegions()) < 1:
                cls.Factions[i].IsDead = True
                cls.Factions[i].IsPlayable = False
                deadFactions += 1
        Log.InfoIf(deadFactions > 0, f"Initialized {deadFactions} dead factions")
        shadowFactions = []
        for faction in [f for f in cls.Factions if f.IsPlayable or f.IsDead]:
            shadowFactions.append(faction.createShadowFaction())
        cls.Factions += shadowFactions
        Log.Info(f"Initialized {len(shadowFactions)} shadow factions")

        Log.Info("Initializing Regions")
        for i, region in enumerate(cls.Regions):
            cls.Names.append(Name(99999999-i, "dummy", "surname", f"of {region.NameCity}"))
            regionTiles = Get.AllTilesByRegion(region)
            cls.Regions[i].PositionsAccessibleLand = [t.toPosition() for t in regionTiles if not t.IsCity and not t.IsPort and t.IsAccessible]
            try:
                cls.Regions[i].PositionCity = [t for t in regionTiles if t.IsCity][0].toPosition()
            except IndexError:
                Log.Error(f"{region.IdRegion} has no city position (probably wrong region RGB or black dot on map_regions.tga is not RGB 0 0 0 (even though it looks black), there is a duplicate RGB for regions, or the city is too close to a port or the coast")
            try:
                cls.Regions[i].PositionPort = [t for t in regionTiles if t.IsPort][0].toPosition()
            except IndexError:
                pass  # Region has no port
            cls.Regions[i].SettlementLevel = \
            [s for s in cls.SettlementLevels if s.MinPop <= region.Population <= s.MaxPop][0]
            cls.Regions[i].StarterBuildingsCount = Stringtools.intWithPossibleRange(region.SettlementLevel.StarterBuildingsCount)
            while len(region.Buildings) < region.StarterBuildingsCount:
                buildings = cls.Regions[i].getAddableBuildings()
                cls.Regions[i].Buildings.append(random.choice(buildings).Id)

        Log.Info("Initializing Factions")
        superfactions = list(set([f.Superfaction for f in Get.AllFactions() if f.Superfaction is not None]))
        for i, faction in enumerate([f for f in cls.Factions]):
            if not faction.IsShadowFaction and not faction.IsDead:  # Must not be in list comprehension due to index
                capital = faction.getStartingRegions()[0]
                cls.Factions[i].IsSuperFaction = faction.Id in superfactions
                cls.Factions[i].IsPlayable = False if faction.IsSuperFaction or faction.IsSlave or faction.IsDead else True
                if not faction.IsShadowFaction:  # No hording for shadow factions
                    cls.Factions[i].CanHorde = faction.getCulture().CanHorde
                if faction.Difficulty != 0:
                    cls.Factions[i].Difficulty = max(4 - len(faction.getStartingRegions()), 0)
                takenNames = []
                prename = faction.getRandomName("characters")
                surname = None  # Leader should not have surname otherwise problem with family tree
                # Add leader
                if faction.LeaderName is not None:
                    prename = faction.LeaderName
                    if " " in faction.LeaderName:
                        prename = faction.LeaderName.split(" ")[0]
                age = random.randint(40, 50) if faction.LeaderAge is None else faction.LeaderAge
                age = 36 if age < 36 else age  # Otherwise his heir will be too young
                leader = Character(prename, surname, True, False, age, faction.getCapital().PositionCity,
                                   Army(faction, True), faction, faction)
                cls.Factions[i].NamedCharacters.append(leader)
                cntCitiesWithGovernor = 1
                # Add heir
                prename = faction.getRandomName("characters")
                heirSurname = faction.getRandomName("surname")
                if faction.HeirName is not None:
                    prename = faction.HeirName
                    if " " in faction.HeirName:
                        prename = faction.HeirName.split(" ")[0]
                        heirSurname = faction.HeirName.split(" ")[1]
                if len(faction.getStartingRegions()) > 1:
                    pos = faction.getStartingRegions()[1].PositionCity
                    cntCitiesWithGovernor += 1
                    unitsCount = None
                else:
                    pos = capital.getRandomPositionLand()
                    unitsCount = 0
                age = age - 18 if faction.HeirAge is None else faction.HeirAge
                takenNames.append("%s %s" % (prename, heirSurname))
                heir = Character(prename, heirSurname, False, True, age, pos, Army(faction, True, unitsCount), faction, faction)
                cls.Factions[i].NamedCharacters.append(heir)
                Log.ErrorIf(Get.Setting("InitGeneralsMin") < 2, "InitGeneralsMin must be >= 2")
                Log.ErrorIf(Get.Setting("InitGeneralsMax") > 6, "InitGeneralsMax must be <= 6")
                # Add other named characters
                capGenerals = faction.countRegions()
                capGenerals = Get.Setting("InitGeneralsMin") if Get.Setting("InitGeneralsMin") > faction.countRegions() else capGenerals
                capGenerals = Get.Setting("InitGeneralsMax") if Get.Setting("InitGeneralsMax") < faction.countRegions() else capGenerals
                while len(cls.Factions[i].NamedCharacters) < capGenerals:
                    while True:
                        prename, surname = faction.getRandomName("characters"), faction.getRandomName("surname")
                        if "%s %s" % (prename, surname) not in takenNames:
                            break
                    if len(faction.getStartingRegions()) > cntCitiesWithGovernor:
                        pos = faction.getStartingRegions()[cntCitiesWithGovernor].PositionCity
                        cntCitiesWithGovernor += 1
                        unitsCount = None
                    else:
                        pos = capital.getRandomPositionLand()
                        unitsCount = 0
                    age = random.randint(20, 50)
                    takenNames.append("%s %s" % (prename, surname))
                    newguy = Character(prename, surname, False, False, age, pos, Army(faction, True, unitsCount), faction, faction)
                    cls.Factions[i].NamedCharacters.append(newguy)
                    leaderAndHeir = cls.Factions[i].NamedCharacters[0:2]
                    theRest = cls.Factions[i].NamedCharacters[2:]
                    theRest.sort(key=lambda x: x.Age, reverse=True)
                    cls.Factions[i].NamedCharacters = leaderAndHeir + theRest
                # Add women
                leaderAgeOffset = 0
                isLeadersWife = True
                for character in cls.Factions[i].NamedCharacters:
                    while True:
                        name = faction.getRandomName("women")
                        if name not in [c.Name for c in cls.Factions[i].FemaleCharacters] \
                                and name not in [c.Name for c in cls.Factions[i].NamedCharacters]:
                            break
                    leaderAge = cls.Factions[i].NamedCharacters[0].Age
                    womanAge = leaderAge if isLeadersWife else leaderAge - 18 - leaderAgeOffset
                    cls.Factions[i].FemaleCharacters.append(CharacterFemale(name, character.Surname, womanAge))
                    leaderAgeOffset += 1
                    isLeadersWife = False
                # Add non family generals
                while cntCitiesWithGovernor < len(faction.getStartingRegions()):
                    pos = faction.getStartingRegions()[cntCitiesWithGovernor].PositionCity
                    while True:
                        name = faction.getRandomName("characters")
                        if name not in [c.Name for c in cls.Factions[i].NamedCharacters] \
                                and name not in [c.Name for c in cls.Factions[i].FemaleCharacters]:
                            break
                    newGeneral = General(name, pos, Army(faction, False), faction, faction)
                    cls.Factions[i].Generals.append(newGeneral)
                    cntCitiesWithGovernor += 1
                agents = Get.Setting("InitAgents").split(",") if "," in Get.Setting("InitAgents") else [Get.Setting("InitAgents")]
                for n in range(0, Get.Setting("InitAgentsPerFaction")):
                    agentType = random.choice(agents).strip()
                    pos = random.choice(faction.getStartingRegions()).getRandomPositionLand()
                    while True:
                        name = faction.getRandomName("characters")
                        if name not in [c.Name for c in cls.Factions[i].NamedCharacters] \
                                and name not in [c.Name for c in cls.Factions[i].FemaleCharacters]:
                            break
                    agentSurname = faction.getRandomName("surname")
                    if agentType == "merchant":
                        agentSurname = [n for n in Get.AllNames() if n.Id == f"of_{capital.IdCity}"][0].Id
                    agent = Agent(name, agentSurname, agentType, pos)
                    cls.Factions[i].Agents.append(agent)
                cls.Factions[i].initFamilyTree()
                if faction.IsSlave:
                    cls.Factions[i].NamedCharacters = []
                    for region in faction.getStartingRegions():
                        rebelFaction = [r for r in cls.RebelFactions if r.Id == region.RebelFaction][0]
                        subfaction = Get.FactionById(rebelFaction.SubfactionId)
                        while True:
                            prename = subfaction.getRandomName("characters")
                            surname = subfaction.getRandomName("surname")
                            if "%s %s" % (prename, surname) not in takenNames:
                                break
                        takenNames.append("%s %s" % (prename, surname))
                        armyUnitPool = [u for u in rebelFaction.Units]
                        assert len(armyUnitPool) > 0
                        targetUnitCount = Stringtools.intWithPossibleRange(region.SettlementLevel.RebelUnitCount)
                        armyUnits = []
                        for n in range(0, targetUnitCount):
                            unitId = random.choice(armyUnitPool)
                            unit = [u for u in cls.Units if u.Id == unitId][0]
                            exp = Stringtools.intWithPossibleRange(region.SettlementLevel.RebelUnitExp)
                            armourLvl = Stringtools.intWithPossibleRange(region.SettlementLevel.RebelUnitArmourLvl)
                            weaponLvl = Stringtools.intWithPossibleRange(region.SettlementLevel.RebelUnitWeaponLvl)
                            armyUnits.append(ArmyUnit(unit, exp, armourLvl, weaponLvl))
                        army = Army(faction, True, armyunits=armyUnits)
                        newRebelCharacter = Character(prename, surname, False, False, random.randint(20, 60),
                                               Position(region.PositionCity.X, region.PositionCity.Y), army, faction,
                                               subfaction)
                        cls.Factions[i].NamedCharacters.append(newRebelCharacter)
                # Faction bonuses in buildings
                if len(faction.BonusBuildingEffects) > 0:
                    for bonusBuildingEffect in faction.BonusBuildingEffects:
                        chain, capabilityString = bonusBuildingEffect.split(":")
                        for i, building in enumerate(cls.Buildings):
                            if building.BuildingChain == chain:
                                cls.Buildings[i].CapabilityStrings.append(f"{capabilityString} requires factions {{ {faction.Id}, }}")

        cls.Resources.sort(key=lambda x: x.DepositCap)
        # Distribute capped resources across possible regions
        for resource in [r for r in cls.Resources if r.IsOnMap and r.DepositCap > 0]:
            cls.ResourceCounts[resource.Id] = 0
            while cls.ResourceCounts[resource.Id] < resource.DepositCap:
                possibleRegions = [region for region in Get.AllRegions() if region.ResourcePool in resource.ResourcePools and len(region.PositionsResources) < region.ResourceSlots]
                if len(possibleRegions) == 0:
                    Log.Warn(f"Resource {resource} has no possible regions left ({cls.ResourceCounts[resource.Id]}/{resource.DepositCap} placed on map)")
                    break
                if len(possibleRegions) > 0:
                    region = random.choice(possibleRegions)
                    idx = cls.Regions.index(region)
                    cls.Regions[idx].addResource(resource)
                    cls.ResourceCounts[resource.Id] += 1

        # Distribute uncapped resources across regions with free slots
        for i, region in enumerate(cls.Regions):
            cls.Regions[i].addResource(Get.ResourceById("slaves"))  # hidden slave resource must be in each region
            if Get.FactionById(region.FactionNative).Culture == "roman":
                cls.Regions[i].addResource(Get.ResourceById("italy"))
            nonResources = len([r for r in cls.Regions[i].PositionsResources if not r.Resource.IsOnMap])  # eg +1 because each region has a slave resource
            if len(region.PositionsAccessibleLand) == 0:
                Log.Error("Region %s has no accessible land positions" % region)
            elif 0 < len(region.PositionsAccessibleLand) < 5:
                Log.Warn("Region %s has only %s accessible land positions" % (region, len(region.PositionsAccessibleLand)))
            if len(region.PositionsResources) < region.ResourceSlots + nonResources:
                possibleResources = [r for r in cls.Resources if r.IsOnMap and r.DepositCap < 1 and region.ResourcePool in r.ResourcePools]
                Log.ErrorIf(len(possibleResources) == 0, "No possible resources left for %s, pool %s" % (region, region.ResourcePool))
                res = random.choice(possibleResources)
                cls.Regions[i].addResource(res)

        stdCostTower = max(set([c.CostTower for c in Get.AllCultures()]), key=[c.CostTower for c in Get.AllCultures()].count)
        stdCostFort = max(set([c.CostFort for c in Get.AllCultures()]), key=[c.CostFort for c in Get.AllCultures()].count)
        stdCostSpy = max(set([c.CostSpy for c in Get.AllCultures()]), key=[c.CostSpy for c in Get.AllCultures()].count)
        stdCostAssassin = max(set([c.CostAssassin for c in Get.AllCultures()]), key=[c.CostAssassin for c in Get.AllCultures()].count)
        stdCostDiplomat = max(set([c.CostDiplomat for c in Get.AllCultures()]), key=[c.CostDiplomat for c in Get.AllCultures()].count)
        stdCostMerchant = max(set([c.CostMerchant for c in Get.AllCultures()]), key=[c.CostMerchant for c in Get.AllCultures()].count)
        for i, culture in enumerate(cls.Cultures):
            if stdCostTower != culture.CostTower:
                pct = int((stdCostTower - culture.CostTower) * 100 / stdCostTower) * -1
                cls.Cultures[i].BonusLabels.append(f"{pct}% to watchtower cost")
            if stdCostFort != culture.CostFort:
                pct = int((stdCostFort - culture.CostFort) * 100 / stdCostFort) * -1
                cls.Cultures[i].BonusLabels.append(f"{pct}% to fort cost")
            if stdCostSpy != culture.CostSpy:
                pct = int((stdCostSpy - culture.CostSpy) * 100 / stdCostSpy) * -1
                cls.Cultures[i].BonusLabels.append(f"{pct}% to spy recruitment cost")
            if stdCostAssassin != culture.CostAssassin:
                pct = int((stdCostAssassin - culture.CostAssassin) * 100 / stdCostAssassin) * -1
                cls.Cultures[i].BonusLabels.append(f"{pct}% to assassin recruitment cost")
            if stdCostDiplomat != culture.CostDiplomat:
                pct = int((stdCostDiplomat - culture.CostDiplomat) * 100 / stdCostDiplomat) * -1
                cls.Cultures[i].BonusLabels.append(f"{pct}% to diplomat recruitment cost")
            if stdCostMerchant != culture.CostMerchant:
                pct = int((stdCostMerchant - culture.CostMerchant) * 100 / stdCostMerchant) * -1
                cls.Cultures[i].BonusLabels.append(f"{pct}% to merchant recruitment cost")

        countRegionsWithPortCoordinates = len([r for r in cls.Regions if r.PositionPort is not None])
        countPortPixelsMapRegionsTga = OStools.countPixelByRGB(Globals.PathMapsBase / "map_regions.tga", 255, 255, 255)
        Log.Info(f"Regions with port coordinates: {countRegionsWithPortCoordinates}")
        Log.Info(f"Port pixels map_regions.tga: {countPortPixelsMapRegionsTga}")
        Log.WarnIf(countRegionsWithPortCoordinates != countPortPixelsMapRegionsTga, f"See mismatch above!")
        cls.BuildingChains.sort(key=lambda x: x.BaseMoney)
        cls.Units.sort(key=lambda x: x.CostRecruit)

    @classmethod
    def evaluate(cls):
        if not Get.Setting("SkipEvaluation"):
            Log.Info("Running evaluations")
            for faction in [f for f in cls.Factions if not f.IsSlave and f.IsPlayable]:
                recruitableUnits = [u for u in cls.Units if faction.Id in u.Ownership and u.BuildingChain is not None]
                for bchain in [c for c in cls.BuildingChains if c.RecruitNewUnitEachLvl]:
                    recruitableHere = [u for u in recruitableUnits if u.BuildingChain == bchain.Id and faction.Id in u.Ownership]
                    used = []
                    lastCost = 0
                    lastName = ""
                    for i in range(1, 6):
                        txt = f"RecrTree {faction.Id} {bchain.Id} {i}:"
                        try:
                            units = [u for u in recruitableHere if u.BuildingChainLvl == i]
                            unit = units[0]
                            Log.Info(f"{txt} {unit.Id} ({unit.CostRecruit})")
                            Log.WarnIf(len(units) > 1, f"{txt} ... but more than 1 unit recruitable here!")
                            used.append(unit.Id)
                            Log.WarnIf(lastCost > unit.CostRecruit, f"{txt} ... but costs fewer than last unit!")
                            Log.WarnIf(lastName == unit.Id, f"{txt} ... but is probably same as last unit!")
                            lastCost = unit.CostRecruit
                            lastName = unit.Id
                        except IndexError:
                            Log.Warn(f"{txt} No unit!")
                    excess = [u.Id for u in recruitableHere if u.Id not in used]
                    Log.InfoIf(len(excess) > 0, f"RecrTree {faction.Id} {bchain.Id} Excess: " + ", ".join(excess))
            unitsByOccurance = [u for u in Get.AllUnits() if u.Category in ["cavalry", "infantry"] and "peasant" not in u.Id]
            unitsByOccurance.sort(key=lambda x: len(x.Ownership), reverse=True)
            Log.Info("Most common regular units (faction count):")
            for i in range(0, 10):
                Log.Info(f"{i+1}. {unitsByOccurance[i].Id} ({len(unitsByOccurance[i].Ownership)})")
            Log.Info("Buildings Costs")
            for building in Get.AllBuildings():
                Log.Info(f"{building.Level} {building.Id} {building.CostMoney} denarii {building.CostRounds} rounds")
        else:
            Log.Info("Evaluation skipped, set SkipEvaluation to TRUE in Config, Settings if you want to see balancing stats etc.")

    @classmethod
    def runChecks(cls):
        cntFactionsSelection = len([f for f in Get.AllFactionsPlayable() if not f.ForceUnplayable])
        Log.WarnIf(cntFactionsSelection > 80, f"{cntFactionsSelection} factions are playable and can be selected in the campaign menu, but due to an engine bug campaign selection screen will freeze if more than 80 factions can be selected")

    @classmethod
    def addSpecials(cls):
        if Get.Setting("EnableGarrisons"):
            garrisonchain = BuildingChain(999, "garrisonchain", "Garrison", 1, 3000, False, "government", "all", None, False, "core", False, False, None)
            garrisonchain.PlayerOnly = True
            name = "Recruit an emergency garrison"
            descr = "Recruits an emergency garrison, but risks riots."
            garrisonchainbldng = Building(998, "garrison", "garrisonchain", 0, name, None,	None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, descr, None, None)
            World.BuildingChains.append(garrisonchain)
            World.Buildings.append(garrisonchainbldng)
        if Get.Setting("EnableSettlementAutonomy"):
            autonomychain = BuildingChain(997, "autonomychain", "Autonomy", 1, 0, False, "government", "all", None, False, "core", False, False, None)
            autonomychain.PlayerOnly = True
            name = "Grant this settlement autonomy"
            descr = "Releases settlement into autonomy. you lucrate between 10000 and 1000 denarii from that. The new settlements owners will hate your guts though."
            autonomybldng = Building(999, "autonomy", "autonomychain", 0, name, None,	None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, descr, None, None)
            World.BuildingChains.append(autonomychain)
            World.Buildings.append(autonomybldng)
        if Get.Setting("EnableAIAssist"):
            aiassistchain = BuildingChain(996, "aiassistchain", "AI Assist", 1, 0, False, "government", "all", None, False, "core", False, False, None)
            aiassistchain.AiOnly = True
            aiassistchain.IsConstructable = False
            name = "AI Assist"
            descr = "Assist the AI."
            aiassistbldng = Building(995, "aiassist", "aiassistchain", 0, name, None,	None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, descr, None, None)
            aiassistbldng.FactionWideCapabilities.append("law_bonus bonus 50")
            World.BuildingChains.append(aiassistchain)
            World.Buildings.append(aiassistbldng)
        OStools.CleanDir("world/maps/campaign/imperial_campaign/FactionRespawnInCapital")
        if Get.Setting("EnableFactionRespawnInCapital"):
            folderPath = Globals.PathModMapsCampaign / "FactionRespawnInCapital"
            for faction in Get.AllFactionsPlayable():
                filePath = folderPath / f"{faction.Id}.txt"
                Path(folderPath).mkdir(parents=True, exist_ok=True)
                Path(filePath).touch(exist_ok=True)
                with open(filePath, "w") as f:
                    f.write(f"\nscript")
                    f.write(f"\n\tif not FactionIsAlive {faction.Id}")
                    f.write(f"\n\tand SettlementName {faction.getCapital().IdCity}")
                    f.write(f"\n\t\treturn true")
                    f.write(f"\n\tend_if")
                    f.write(f"\n\treturn false")
                    f.write(f"\nend_script\n")
            for spawnFaction in Get.AllDeadFactionsExShadow():
                filePath = folderPath / f"{spawnFaction.Id}.txt"
                Path(folderPath).mkdir(parents=True, exist_ok=True)
                Path(filePath).touch(exist_ok=True)
                with open(filePath, "w") as f:
                    f.write(f"\nscript")
                    for NativeRegion in spawnFaction.getNativeRegions():
                        f.write(f"\n\tif not FactionIsAlive {spawnFaction.Id}")
                        f.write(f"\n\tand SettlementName {NativeRegion.IdCity}")
                        f.write(f"\n\t\treturn true")
                        f.write(f"\n\tend_if")
                    f.write(f"\n\treturn false")
                    f.write(f"\nend_script\n")
