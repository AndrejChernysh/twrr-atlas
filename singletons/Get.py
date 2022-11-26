import PIL

import Globals
import Log
import classes.Building as Building
import classes.BuildingChain as BuildingChain
import classes.Culture as Culture
import classes.Faction as Faction
import classes.Tile as Tile
import classes.Name as Name
import classes.Region as Region
import classes.Landmark as Landmark
import classes.Resource as Resource
import classes.SettlementLevel as SettlementLevel
import classes.Unit as Unit
import classes.MercPool as MercPool
import classes.Religion as Religion
import classes.RebelFaction as RebelFaction
import classes.Setting as Setting
import classes.Mount as Mount
import classes.Message as Message
import singletons.Settings as Settings
import singletons.World as World
import singletons.WorldMap as WorldMap
import random


def AllBuildingChains() -> list[BuildingChain.BuildingChain]:
    return [bc for bc in World.World.BuildingChains]


def AllBuildings() -> list[Building.Building]:
    return [b for b in World.World.Buildings]


def AllBuildingsWithVariableName() -> list[Building.Building]:
    return [b for b in AllBuildings() if b.Name.count("%") == 2]


def AllCultures() -> list[Culture.Culture]:
    return [c for c in World.World.Cultures]


def AllCustomCapabilities():
    usedCapabilityIds = []
    result = []
    allCustomCapabilities = [b.CustomCapability for b in AllBuildings() if b.CustomCapability is not None]
    for capability in allCustomCapabilities:
        if capability.Id not in usedCapabilityIds:
            result.append(capability)
            usedCapabilityIds.append(capability.Id)
    return result


def AllExclusiveTags() -> list[str]:
    tags = []
    for buildingChain in World.World.BuildingChains:
        if buildingChain.ExclusiveTag is not None and buildingChain.ExclusiveTag not in tags:
            tags.append(buildingChain.ExclusiveTag.strip())
    return tags


def AllRebelFactions() -> list[RebelFaction.RebelFaction]:
    return [r for r in World.World.RebelFactions]


def AllFactionIds(isPlayable=None) -> list[Faction.Faction]:
    if isPlayable is None:
        return [f.Id for f in World.World.Factions]
    elif isPlayable == True:
        return [f.Id for f in World.World.Factions if f.IsPlayable]
    elif isPlayable == False:
        return [f.Id for f in World.World.Factions if not f.IsPlayable]


def AllFactions() -> list[Faction.Faction]:
    return [f for f in World.World.Factions]


def AllFactionsPlayable() -> list[Faction.Faction]:
    return [f for f in World.World.Factions if f.IsPlayable]


def AllDeadFactionsExShadow() -> list[Faction.Faction]:
    return [f for f in World.World.Factions if f.IsDead and not f.IsShadowFaction]


def AllFactionsSortByIndex() -> list[Faction.Faction]:
    result = [f for f in World.World.Factions]
    result.sort(key=lambda x: x.Index)
    return result


def AllFactionsExceptFaction(faction: Faction.Faction) -> list[Faction.Faction]:
    return [f for f in World.World.Factions if not faction == f]


def AllFactionsNonSlave() -> list[Faction.Faction]:
    return [f for f in World.World.Factions if not f.IsSlave]


def AllFactionsNonSlaveSortByLogoIndex() -> list[Faction.Faction]:
    result = [f for f in World.World.Factions if not f.IsSlave]
    result.sort(key=lambda x: x.Index)
    return result


def AllFactionsSortByLogoIndex() -> list[Faction.Faction]:
    result = [f for f in World.World.Factions]
    result.sort(key=lambda x: x.Index)
    return result


def AllMercPools() -> list[MercPool.MercPool]:
    return [f for f in World.World.MercPools]


def AllMercPoolIds() -> list[str]:
    return list(set([m.Id for m in AllMercPools()]))


def DescrSMFactionLogosIconEntries() -> list[str]:
    factions = [f for f in World.World.Factions]
    factions.sort(key=lambda x: x.IndexIcon)
    result = []
    for i in range(0, 500):
        faction = FactionByIndexIcon(i)
        if faction is not None:
            result.append(f"{faction.Id}.tga\t;Index {faction.IndexIcon}")
        else:
            result.append("slave.tga")
    return result


def AllLandmarks() -> list[Landmark.Landmark]:
    return [f for f in World.World.Landmarks]


def AllNames() -> list[Name.Name]:
    return [n for n in World.World.Names]


def AllNamesDistinct() -> list[Name.Name]:
    distinctNameIds = []
    distinctNames = []
    for name in AllNames():
        if name.Id not in distinctNameIds:
            distinctNameIds.append(name.Id)
            distinctNames.append(name)
    return distinctNames


def AllReligions() -> list[Religion.Religion]:
    return [r for r in World.World.Religions]


def AllRegions() -> list[Region.Region]:
    return [r for r in World.World.Regions]


def AllRegionsWithPorts() -> list[Region.Region]:
    return [r for r in AllRegions() if r.PositionPort is not None]


def AllResources() -> list[Resource.Resource]:
    return [r for r in World.World.Resources]


def AllResourcePools() -> list[str]:
    resourcePools = []
    for resource in World.World.Resources:
        for pool in resource.ResourcePools:
            if pool not in resourcePools:
                resourcePools.append(pool)
    return resourcePools


def AllSettingNames() -> list[Setting.Setting]:
    return [s.Setting for s in Settings.Settings.Settings]


def AllSettlementLevels() -> list[SettlementLevel.SettlementLevel]:
    World.World.SettlementLevels.sort(key=lambda x: x.Level)
    return [sl for sl in World.World.SettlementLevels]


def AllTilesByRegion(region: Region.Region) -> list[Tile.Tile]:
    return [t for t in WorldMap.WorldMap.Tiles if t.RegionId == region.IdRegion]


def AllUnits() -> list[Unit.Unit]:
    return [u for u in World.World.Units]


def BuildingById(id: str) -> Building.Building:
    try:
        return [b for b in World.World.Buildings if b.Id == id][0]
    except IndexError:
        Log.Error(f"Could not get building by Id {id}")


def BuildingChainById(id: str) -> BuildingChain.BuildingChain:
    return [bc for bc in World.World.BuildingChains if bc.Id == id][0]


def BuildingsByBuildingChainId(id: str) -> list[Building.Building]:
    return [b for b in World.World.Buildings if b.BuildingChain == id]


def CultureById(id) -> Culture.Culture:
    return [c for c in World.World.Cultures if c.Id == id][0]


def DescrStratSuperfactionSetupEntries() -> str:
    result = []
    for sf in set([sf.Superfaction for sf in World.World.Factions if sf.Superfaction is not None]):
        result.append("superfaction_setup %s" % sf)
        result.append("default_hostile slave")  # TODO Add neighbours
        for minion in [f for f in World.World.Factions if f.Superfaction == sf]:
            # TODO Randomize missions
            target = random.choice([r for r in World.World.Regions if FactionById("slave").getStartingRegions()])
            result.append("\nmission_queue %s\n{\n\t%s %s\n}" % (minion.Id, "major_reward 10 Take_City", target.IdCity))
    return "\n".join(result)


def Messages() -> list[Message.Message]:
    return World.World.Messages


def FactionById(id: str) -> Faction.Faction:
    try:
        return [f for f in World.World.Factions if f.Id == id][0]
    except IndexError:
        Log.Error(f"Get.FactionById() could not find faction with ID {id}")


def FactionByIndex(idx: int):
    try:
        return [f for f in World.World.Factions if f.Index == idx][0]
    except IndexError:
        return None


def FactionByIndexIcon(idx: int):
    try:
        return [f for f in World.World.Factions if f.IndexIcon == idx][0]
    except IndexError:
        return None


def FactionsByCulture(culture: str):
    return [f for f in World.World.Factions if f.Culture == culture]


def FactionIdsPlayable() -> list[str]:
    return [f.Id for f in World.World.Factions if f.IsPlayable and not f.IsSlave and not f.ForceUnplayable]


def FactionIdsNonPlayable() -> list[str]:
    return [f.Id for f in World.World.Factions if not f.IsPlayable or f.IsSlave or f.ForceUnplayable]


def MercPoolUnitsByMercPoolId(mercPoolId: str) -> list[MercPool]:
    return [u for u in AllMercPools() if u.Id == mercPoolId]


def ReligionById(id: str) -> Religion.Religion:
    return [r for r in AllReligions() if r.Id == id][0]


def ReligionByFaction(faction: Faction) -> Religion:
    try:
        return [r for r in AllReligions() if r.Id == faction.Religion][0]
    except IndexError:
        Log.Error(f"Faction {faction} has no valid religion")


def RegionByRGB(r: int, g: int, b: int) -> Region.Region:
    return [reg for reg in World.World.Regions if reg.R == r and reg.G == g and reg.B == b][0]


def RegionIdByTgaXY(x: int, y: int, noOffset=False):
    mapRegionsTga = PIL.Image.open(Globals.PathMapsBase / "map_regions.tga")
    r, g, b = mapRegionsTga.getpixel((x, y))
    rgbc = r * 1000000 + g * 1000 + b
    if rgbc == 255255255 or rgbc == 0:
        if noOffset:
            return None
        results = []
        for oX in [-1, 0, 1]:
            for oY in [-1, 0, 1]:
                try:
                    offsetRegion = RegionIdByTgaXY(x + oX, y + oY, noOffset=True)
                    if offsetRegion is None:
                        continue
                    results.append(RegionIdByTgaXY(x + oX, y + oY, noOffset=True).IdRegion)
                except:
                    pass
        try:
            return max(set(results), key=results.count)
        except ValueError:
            Log.Error(f"Two or more regions share the same RGB")
    try:
        return RegionByRGB(r, g, b)
    except:
        return None


def RegionsByOwnerFaction(faction: Faction.Faction) -> list[Region.Region]:
    return [r for r in World.World.Regions if r.FactionOwner == faction.Id]


def RegionIdsByMercPoolIdSpaceSeparatedString(mercPoolId: str) -> str:
    return " ".join([r.IdRegion for r in AllRegions() if r.MercPoolId == mercPoolId])


def ResourceById(id: str) -> Resource.Resource:
    return [r for r in World.World.Resources if r.Id == id][0]


def ResourcesHidden() -> list[Resource.Resource]:
    return [r for r in AllResources() if r.IsHidden]


def ResourcesNonHidden() -> list[Resource.Resource]:
    return [r for r in AllResources() if not r.IsHidden]


def OtherReligionsSameGroupLike(religionId: str) -> list[Religion.Religion]:
    religion = ReligionById(religionId)
    return [r for r in AllReligions() if r.Group == religion.Group and not r.Id == religion.Id]


def ReligionIdsAsCommaSeparatedListExcept(religionId: str) -> str:
    return ", ".join([r.Id for r in AllReligions() if not r.Id == religionId])


def MountById(id: str) -> Mount.Mount:
    try:
        return [m for m in World.World.Mounts if m.Id == id][0]
    except IndexError:
        Log.Error(f"Could not find Mount {id}")


def Setting(setting: str):  # No return type because it can be either Bool, Str or Int
    return Settings.Settings.get(setting)


def SettingAndMultiply(setting: str, multiplicator: int):  # No return type because it can be either Bool, Str or Int
    return Settings.Settings.get(setting) * multiplicator


def TileByXY(x: int, y: int):
    return [t for t in WorldMap.WorldMap.Tiles if t.X == x and t.Y == y][0]


def UnitById(id: str):
    return [u for u in AllUnits() if u.Id == id][0]


def UnitsByModelId(modelId: str):
    return [u for u in AllUnits() if u.Soldier == modelId]


def AllFactionsByCultureId(cultureId: str):
    return [f for f in AllFactions() if f.Culture == cultureId]


def DMBTextureEntries(modelId: str, isForAllFactions=False):
    unitsWithModelId = UnitsByModelId(modelId)
    if isForAllFactions:
        ownerFactions = AllFactions()
    else:
        ownerFactions = []
        for unit in unitsWithModelId:
            for faction in unit.GetOwnershipFactions():
                if faction not in ownerFactions:
                    ownerFactions.append(faction)
        if len(ownerFactions) == 0:  # maybe the model is for a general unit?
            cultures = [c for c in AllCultures() if c.BMGeneral == modelId or c.BMNamedCharacter == modelId]
            if len(cultures) > 0:
                for culture in cultures:
                    for faction in AllFactionsByCultureId(culture.Id):
                        ownerFactions.append(faction)
        Log.ErrorIf(len(ownerFactions) == 0, f"Model {modelId} is referenced in DMBTextureEntries() inside a file but appears to be not referenced in Configuration.xlsx -> Units")
    for textureCode in set([f.TextureCode for f in ownerFactions]):
        Log.WarnIfNoFile(Globals.PathRootMod / "textures_battle_units", f"{modelId}_{textureCode}.tga.dds")
    result = [f"texture data/textures_battle_units/{modelId}_{ownerFactions[0].TextureCode}.tga"]
    for faction in ownerFactions:
        result.append(f"texture {faction.Id}, data/textures_battle_units/{modelId}_{faction.TextureCode}.tga")
    return "\n".join(result)
