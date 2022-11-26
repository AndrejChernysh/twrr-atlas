import Log
from classes.FamilySubTree import FamilySubTree
from classes.AIProfile import AIProfile
import classes.Region as Region
import classes.Agent as Agent
import classes.General as General
import classes.Character as Character
import classes.CharacterFemale as CharacterFemale
import classes.Culture as Culture
import classes.RGB as RGB
import singletons.Get as Get
import Stringtools
import Convert
import random


class Faction:

    _UIDPrefix = "FA"  # Must be unique across all classes!

    def __init__(self, uid, id, superfaction, name, culture, religion, color1, color2, money, leadername, leaderby, heirname, heirby, diplomacyattitude, index, campaigndescr, adjective, texturecode, texturecodesf, namerebels, aihostility, bonusbuildingeffect, bonuslabels, forceunplayable):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(id is None, f"Faction {uid} has no ID")
        Log.ErrorIf(name is None, f"Faction {id} has no Name")
        Log.ErrorIf(culture is None, f"Faction {id} has no Culture")
        Log.ErrorIf(religion is None, f"Faction {id} has no Religion")
        Log.ErrorIf(color1 is None, f"Faction {id} has no Color1")
        Log.ErrorIf(color2 is None, f"Faction {id} has no Color2")
        Log.ErrorIf(money is None, f"Faction {id} has no Money")
        Log.ErrorIf(diplomacyattitude is None, f"Faction {id} has no DiplomacyAttitude")
        Log.ErrorIf(index is None, f"Faction {id} has no Index")
        Log.ErrorIf(campaigndescr is None, f"Faction {id} has no CampaignDescr")
        Log.ErrorIf(adjective is None, f"Faction {id} has no Adjective")
        Log.ErrorIf(texturecode is None, f"Faction {id} has no TextureCode")
        Log.ErrorIf(texturecodesf is None, f"Faction {id} has no TextureCodeSF")
        Log.ErrorIf(aihostility is None, f"Faction {id} has no AIHostility")
        Log.ErrorIf(forceunplayable is None, f"Faction {id} has no ForceUnplayable")
        self.Id = Convert.Str(id)
        self.Superfaction = Convert.Str(superfaction)
        self.Name = Convert.Str(name)
        self.NameRebels = Convert.Str(namerebels)
        self.Culture = Convert.Str(culture)
        self.Religion = Convert.Str(religion)
        self.Color1: RGB = Convert.RGBFromCommaDelimitedString(color1)
        self.Color2: RGB = Convert.RGBFromCommaDelimitedString(color2)
        self.Money = Stringtools.intWithPossibleRange(money)
        self.LeaderName = Convert.Str(leadername)
        self.LeaderAge = None if leaderby is None else int(Get.Setting("StartDate")) - leaderby
        Log.ErrorIf(self.LeaderAge is not None and self.LeaderAge > 90, f"{self.Id} leader too old: {self.LeaderAge}")
        self.HeirName = Convert.Str(heirname)
        self.HeirAge = None if heirby is None else int(Get.Setting("StartDate")) - heirby
        Log.ErrorIf(self.HeirAge is not None and self.HeirAge > 90, f"{self.Id} heir too old: {self.HeirAge}")
        Log.ErrorIf(self.LeaderAge is not None and self.HeirAge is not None and self.LeaderAge < self.HeirAge + 18,
                    f"{self.Id} leader is not older than heir +18 years")
        self.DiplomacyAttitude = Stringtools.intWithPossibleRange(diplomacyattitude)
        self.Difficulty = 0 if self.Superfaction is not None else 1
        Log.ErrorIf(index is None, f"Faction {self.Id} is missing Index")
        self.Index: int = int(index)
        self.IndexIcon = Convert.Int(index)
        self.IndexBannerlogo = Convert.Int(index)
        self.CampaignDescription: str = "TODO" if campaigndescr is None else campaigndescr
        self.Adjective: str = adjective
        self.TextureCode: str = texturecode
        self.TextureCodeSF: str = texturecodesf
        self.NamedCharacters: list[Character] = []
        self.FemaleCharacters: list[CharacterFemale] = []
        self.Generals: list[General] = []
        self.Agents: list[Agent] = []
        self.FamilyTree: list[FamilySubTree] = []
        self.IsSlave: bool = self.Id == "slave"
        self.IsPlayable: bool = not self.IsSlave
        self.CanCustomBattle: bool = not self.IsSlave
        self.HasFamilyTree: bool = not self.IsSlave
        self.IsSuperFaction: bool = False
        self.HasFamilyTreeJSONString = str(self.HasFamilyTree).lower()
        self.IsShadowFaction: bool = False
        self.ShadowsFactionId: str = ""
        self.ForceUnplayable: bool = forceunplayable
        self.AIProfile: AIProfile = AIProfile(self.Id, Stringtools.intWithPossibleRange(aihostility))
        self.CanHorde: bool = False
        self.BonusBuildingEffects: list[str] = Convert.ListFromCommaDelimitedString(bonusbuildingeffect)
        self.BonusLabels: list[str] = Convert.ListFromCommaDelimitedString(bonuslabels)
        self.IsDead: bool = False

    def __str__(self):
        return self.Id

    def __eq__(self, other):
        return self.Id == other.Id

    def getCanCustomBattleJSONString(self):
        return "true" if self.CanCustomBattle else "false"

    def getSuperFactionString(self) -> str:
        if self.Superfaction is None:
            return ""
        return "\nsuperfaction %s" % self.Superfaction

    def getStartingRegions(self) -> list[Region]:
        return sorted(Get.RegionsByOwnerFaction(self), key=lambda r: r.IsCapital, reverse=True)

    def countRegions(self) -> int:
        return len(self.getStartingRegions())

    def getRandomName(self, type) -> str:
        try:
            return random.choice([n.Id for n in Get.AllNames() if n.Type == type and n.Culture == self.Culture])
        except IndexError:
            exit("Could not find any %s name entries for faction %s" % (type, self))

    def getCapital(self) -> Region:
        try:
            if self.IsShadowFaction:
                return Get.FactionById(self.ShadowsFactionId).getCapital()
            return self.getStartingRegions()[0]
        except IndexError:
            return self.getNativeRegions()[0]

    def getCulture(self) -> Culture:
        return Get.CultureById(self.Culture)

    def getDescrStratAgentsEntry(self) -> str:
        code = ""
        for agent in self.Agents:
            code += agent.getDescrStratString()
        return code

    def initFamilyTree(self):
        if self.HasFamilyTree:
            self.FamilyTree.append(FamilySubTree(self.NamedCharacters[0], self.FemaleCharacters[0], self.FemaleCharacters[1:]))
            for i in range(1, len(self.NamedCharacters)):
                self.FamilyTree.append(FamilySubTree(self.NamedCharacters[i], self.FemaleCharacters[i]))

    def getDescrStratAttitudesEntry(self):
        if self.IsShadowFaction:
            return ""
        result = []
        for otherFaction in Get.AllFactionsExceptFaction(self):
            if not otherFaction.IsShadowFaction and not otherFaction.IsSlave:
                result.append("core_attitudes\t%s,\t%s\t%s" % (self.Id, self.DiplomacyAttitude, otherFaction.Id))
        return "\n".join(result)

    def getDescrStratRelationshipsEntry(self):
        result = []
        for otherFaction in Get.AllFactionsExceptFaction(self):
            if self.IsSlave or otherFaction.IsSlave or (self.Superfaction == otherFaction.Superfaction and not self.Superfaction is None) or self.Superfaction == otherFaction.Id or self.Id == otherFaction.Superfaction or self.Id == otherFaction.ShadowsFactionId:
                relationship = 600 if self.IsSlave or otherFaction.IsSlave or self.Id == otherFaction.ShadowsFactionId else 100
                result.append("faction_relationships\t%s,\t%s\t%s" % (self.Id, relationship, otherFaction.Id))
        return "\n".join(result)

    def getNamedCharacterBodyguardUnit(self, level=1):
        try:
            units = [u for u in Get.AllUnits() if self.Id in u.Ownership and u.NamedCharacterBodyguardLevel == level]
            return units[0]
        except IndexError:
            Log.Error(f"Faction {self} has no units!")

    def getRandomStarterUnitLand(self, recruitmentChain=None):
        units = [u for u in Get.AllUnits() if self.Id in u.Ownership and u.IsStarter]
        if recruitmentChain is not None:
            units = [u for u in units if u.BuildingChain == recruitmentChain]
        Log.ErrorIf(len(units) == 0, f"Could not get any starter units for {self.Id}")
        return random.choice(units)

    def getRandomOtherFactionIdNonSlaveNonShadow(self):
        return random.choice([f.Id for f in Get.AllFactionsNonSlave() if not f.Id == self.Id and not f.IsShadowFaction])

    def getUnits(self):
        return [u for u in Get.AllUnits() if self.Id in u.Ownership]

    def getBonusText(self):
        allBonuses = Get.CultureById(self.Culture).BonusLabels + self.BonusLabels
        return "" if len(allBonuses) == 0 else "\\n".join(allBonuses)

    def getPopulationCount(self):
        return sum([r.Population for r in self.getStartingRegions()])

    def getTroopCount(self):
        cnt = 0
        for character in self.NamedCharacters:
            if character.Army is not None:
                for armyUnit in character.Army.ArmyUnits:
                    cnt += armyUnit.Unit.NumberSoldiers * 2
        for general in self.Generals:
            if general.Army is not None:
                for armyUnit in general.Army.ArmyUnits:
                    cnt += armyUnit.Unit.NumberSoldiers * 2
        return cnt

    def getDescrSMFactionsHordeSection(self):
        unitIds = [u.Id for u in self.getUnits() if u.IsStarter]
        unitIdsList = ",\n\t\t\t\t".join([f"\"{u}\"" for u in unitIds])
        code = f""""horde":
        {{
            "horde units":
            [
                {unitIdsList},
            ],
            "min horde units": 10,
            "max horde units": 20,
            "horde unit reduction per horde": 20,
            "population to horde units": 300,
            "min named characters": 1,
            "max horde unit army percent": 100,
            "horde unit disband per settlement": [ 100, 100, 100, ],
        }},"""
        return code if self.CanHorde else ""

    def getShadowFactionString(self):
        if self.IsShadowFaction or self.IsDead:
            return "\ndead_until_resurrected"  # No re_emergent because all playable factions are re_emergent (respawn)
        return ""

    def createShadowFaction(self):
        rgb1 = self.Color2.toCommaDelimitedString()  # Switched colors
        rgb2 = self.Color1.toCommaDelimitedString()
        uid = self.UID.replace(self._UIDPrefix, "")
        name = self.NameRebels
        tc = self.TextureCodeSF
        bbe = None if len(self.BonusBuildingEffects) < 1 else ",".join(self.BonusBuildingEffects)
        sf = Faction(f"{uid}S", f"{self.Id}_s", self.Superfaction, name, self.Culture, self.Religion, rgb1, rgb2, 9999, None, None, None, None, self.DiplomacyAttitude, self.Index, "", self.Adjective, tc, tc, None, 100, bbe, None, True)
        sf.CanCustomBattle = False
        sf.IsPlayable = False
        sf.IsShadowFaction = True
        sf.IsDead = True
        sf.ShadowsFactionId = self.Id
        sf.IndexIcon = max([f.IndexIcon for f in Get.AllFactions() if not f.IsShadowFaction]) + sf.IndexIcon + 1
        return sf

    def getDescrSMFactionsShadowSection(self):
        code = ""
        if self.IsShadowFaction:
            code = f"""\"shadow faction\": \"{self.ShadowsFactionId}\",
        \"shadow max provinces\": -1,
        \"allow shadow switchback\": false,"""
        elif not self.IsShadowFaction and not self.IsSlave:
            code = f"""\"shadow faction\": \"{self.Id}_s\",
        \"shadow max provinces\": -1,
        \"allow shadow switchback\": false,"""
        return code

    def getAIPersonalityId(self):
        return f"ai_personality_{self.AIProfile.Id}"

    def getNativeRegions(self):
        regions = [r for r in Get.AllRegions() if r.FactionNative == self.Id]
        Log.ErrorIf(len(regions) < 1, f"Faction {self.Id} is expected to have at least 1 native region")
        return regions
