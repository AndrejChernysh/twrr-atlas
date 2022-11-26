
import Convert
import Log
import Translatetools
import singletons.Get as Get
from classes.CustomCapability import CustomCapability


class Building:

    _UIDPrefix = "BC"  # Must be unique across all classes!

    def __init__(self, uid, id, buildingchain, level, name, religion, agent, games, races, wall, tower, gatestrength, gatedefences, law, happiness, trade, growth, wpnsimple, wpnbladed, wpnmissile, wpnsiege, armour, tradefleet, health, farming, road, mine, expbonus, tax, pointsrecr, pointsbuild, tradelvl, morale, reductioncost, reductiontime, description, customcapabilitylabel, requiresbuilding):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(id is None, f"Building {uid} has no ID")
        Log.ErrorIf(buildingchain is None, f"Building {id} has no BuildingChain")
        Log.ErrorIf(level is None, f"Building {id} has no Level")
        Log.ErrorIf(name is None, f"Building {id} has no Name")
        Log.ErrorIf(description is None, f"Building {id} has no Description")
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.BuildingChain = buildingchain
        self.Level = Convert.Int(level)
        self.Religion = Convert.Int(religion)
        self.Agent = Convert.Str(agent)
        self.Games = Convert.Int(games)
        self.Races = Convert.Int(races)
        self.Wall = Convert.Int(wall)
        self.Tower = Convert.Int(tower)
        self.GateStrength = Convert.Int(gatestrength)
        self.GateDefences = Convert.Int(gatedefences)
        self.Law = Convert.Int(law)
        self.Happiness = Convert.Int(happiness)
        self.Trade = Convert.Int(trade)
        self.Growth = Convert.Int(growth)
        self.WpnSimple = Convert.Int(wpnsimple)
        self.WpnBladed = Convert.Int(wpnbladed)
        self.WpnMissile = Convert.Int(wpnmissile)
        self.WpnSiege = Convert.Int(wpnsiege)
        self.Armour = Convert.Int(armour)
        self.TradeFleet = Convert.Int(tradefleet)
        self.Health = Convert.Int(health)
        self.Farming = Convert.Int(farming)
        self.Road = Convert.Int(road)
        self.Mine = Convert.Int(mine)
        self.ExpBonus = Convert.Int(expbonus)
        self.Tax = Convert.Int(tax)
        self.PointsRecr = Convert.Int(pointsrecr)
        self.PointsBuild = Convert.Int(pointsbuild)
        self.TradeLvl = Convert.Int(tradelvl)
        self.Morale = Convert.Int(morale)
        self.ReductionCost = Convert.Int(reductioncost)
        self.ReductionTime = Convert.Int(reductiontime)
        self.Description = Convert.Str(description)
        self.CostMoney = -1
        self.CostRounds = -1
        try:
            self.DescriptionShort = self.Description if "." not in self.Description else "%s." % self.Description.split(".")[0]
        except TypeError:
            Log.Error(f"Building {self.Id} has no Description.")
        self.CustomCapability = None if customcapabilitylabel is None else CustomCapability(customcapabilitylabel)
        self.RequiresBuilding = Convert.Str(requiresbuilding)
        Log.WarnIf(buildingchain != "core_building" and not 0 < level < 6, f"{self} is lvl {level}, will not be shown on building tree (only lvl 1-5)")
        self.FactionWideCapabilities = []
        self.CapabilityStrings: list[str] = []

    def __str__(self):
        return self.Name

    def getBuildingChain(self):
        return Get.BuildingChainById(self.BuildingChain)

    def getCapabilityStringsExRecruit(self):
        CSER = [s for s in self.CapabilityStrings if "fbonus" not in s]  # capability strings excl recruit (these are added from Units)
        if self.Religion is not None:
            for faction in Get.AllFactionsNonSlave():
                CSER.append(f"religious_belief {faction.Religion} {self.Religion} requires factions {{ {faction}, }}")
        if self.Agent is not None:
            CSER.append("agent %s 0" % self.Agent)
            CSER.append("agent_limit_settlement %s 1" % self.Agent)
        if self.Games is not None:
            CSER.append("stage_games %s" % self.Games)
        if self.Races is not None:
            CSER.append("stage_races %s" % self.Races)
        if self.Wall is not None:
            CSER.append("wall_level %s" % self.Wall)
        if self.Tower is not None:
            CSER.append("tower_level %s" % self.Tower)
        if self.GateStrength is not None:
            CSER.append("gate_strength %s" % self.GateStrength)
        if self.GateDefences is not None:
            CSER.append("gate_defences %s" % self.GateDefences)
        if self.Law is not None:
            CSER.append("law_bonus bonus %s" % self.Law)
        if self.Happiness is not None:
            CSER.append("happiness_bonus bonus %s" % self.Happiness)
        if self.Trade is not None:
            CSER.append("trade_base_income_bonus bonus %s" % self.Trade)
        if self.Growth is not None:
            CSER.append("population_growth_bonus bonus %s" % self.Growth)
        if self.WpnSimple is not None:
            CSER.append("weapon_simple %s" % self.WpnSimple)
        if self.WpnBladed is not None:
            CSER.append("weapon_bladed %s" % self.WpnBladed)
        if self.WpnMissile is not None:
            CSER.append("weapon_missile %s" % self.WpnMissile)
        if self.WpnSiege is not None:
            CSER.append("weapon_siege %s" % self.WpnSiege)
        if self.Armour is not None:
            CSER.append("armour %s" % self.Armour)
        if self.TradeFleet is not None:
            CSER.append("trade_fleet %s" % self.TradeFleet)
        if self.Health is not None:
            CSER.append("population_health_bonus bonus %s" % self.Health)
        if self.Farming is not None:
            CSER.append("farming_level %s" % self.Farming)
        if self.Road is not None:
            CSER.append("road_level %s" % self.Road)
        if self.Mine is not None:
            CSER.append("mine_resource %s" % self.Mine)
        if self.ExpBonus is not None:
            CSER.append("recruits_exp_bonus bonus %s" % self.ExpBonus)
        if self.Tax is not None:
            CSER.append("taxable_income_bonus bonus %s" % self.Tax)
        if self.PointsRecr is not None:
            CSER.append("extra_recruitment_points bonus %s" % self.PointsRecr)
        if self.PointsBuild is not None:
            CSER.append("extra_construction_points bonus %s" % self.PointsBuild)
        if self.TradeLvl is not None:
            CSER.append("trade_level_bonus bonus %s" % self.TradeLvl)
        if self.Morale is not None:
            CSER.append("recruits_morale_bonus bonus %s" % self.Morale)
        if self.ReductionCost is not None:  # TODO: Test if works as intended for all buildings equally
            CSER.append("construction_cost_bonus_other bonus %s" % self.ReductionCost)
            CSER.append("construction_cost_bonus_religious  bonus %s" % self.ReductionCost)
        if self.ReductionTime is not None:  # TODO: Test if works as intended for all buildings equally
            CSER.append("construction_time_bonus_other bonus %s" % self.ReductionTime)
            CSER.append("construction_time_bonus_religious bonus %s" % self.ReductionTime)
        if self.CustomCapability is not None:
            CSER.append("dummy %s 1" % self.CustomCapability.Id)
        return CSER

    def getNextLevelBuildingId(self):
        nextBuildings = [b for b in Get.BuildingsByBuildingChainId(self.BuildingChain) if b.Level == self.Level + 1]
        if len(nextBuildings) == 0:
            return ""
        else:
            return nextBuildings[0].Id

    def getSettlementLevel(self):
        maxSettlementLevel = max([s.Level for s in Get.AllSettlementLevels()])
        myLevel = maxSettlementLevel if self.Level > maxSettlementLevel else self.Level
        mySettlementLevel = [s for s in Get.AllSettlementLevels() if s.Level == myLevel][0]
        return mySettlementLevel

    def getConstructionCost(self):
        chain = Get.BuildingChainById(self.BuildingChain)
        lvl = self.Level + 1 if chain.getLowestLevel() == 0 else self.Level
        mp = float(Get.Setting("BuildingsCostMultiplierMoney"))
        self.CostMoney = int((chain.BaseMoney * lvl) ** (1 + (lvl / mp)))
        return self.CostMoney

    def getConstructionTurns(self):
        chain = Get.BuildingChainById(self.BuildingChain)
        lvl = self.Level + 1 if chain.getLowestLevel() == 0 else self.Level
        mp = float(Get.Setting("BuildingsCostMultiplierRounds"))
        self.CostRounds = int(chain.BaseRounds + lvl ** mp) - 1
        return self.CostRounds

    def getUnitsRecruitableHere(self):
        units = [u for u in Get.AllUnits() if self.BuildingChain == u.BuildingChain and self.Level >= u.BuildingChainLvl]
        if len(units) > 0:
            return units

    def getUnitsRecruitableHereWithBonus(self):
        units = [u for u in Get.AllUnits() if self.BuildingChain == u.BuildingChain and self.Level >= u.BuildingChainLvl]
        factionIdsWithBonusForThisBuilding = []
        for factionId in self.getBuildingChain().Ownership:
            faction = Get.FactionById(factionId)
            if len(faction.BonusBuildingEffects) > 0:
                for bonusBuildingEffect in faction.BonusBuildingEffects:
                    if self.BuildingChain in bonusBuildingEffect and "fbonus" in bonusBuildingEffect:
                        factionIdsWithBonusForThisBuilding.append(factionId)
        if len(factionIdsWithBonusForThisBuilding) > 0 and len(units) > 0:
            unitsWithBonusHere = []
            for unit in units:
                for factionIdWithBonusHere in factionIdsWithBonusForThisBuilding:
                    if factionIdWithBonusHere in unit.Ownership and unit not in unitsWithBonusHere:
                        unitsWithBonusHere.append(unit)
            return unitsWithBonusHere

    def getRequiresString(self):
        myBuildingChain = Get.BuildingChainById(self.BuildingChain)
        exemptedCultures = []
        exemptedFactions = []
        clearedFactions = []
        if not myBuildingChain.IsConstructable:
            return "requires hidden_resource nobuild"
        for culture in Get.AllCultures():
            if self.Level > culture.MaxSettlementLvl and not self.BuildingChain == "core_building":
                exemptedCultures.append(culture.Id)
            elif self.Level > culture.MaxSettlementLvl - 1 and self.BuildingChain == "core_building":
                exemptedCultures.append(culture.Id)
        if len(exemptedCultures) > 0:
            for exemptedCulture in exemptedCultures:
                exemptedFactions.extend(Translatetools.translateCultureToFactionsList(exemptedCulture))
            for faction in myBuildingChain.Ownership:
                if faction not in exemptedFactions:
                    clearedFactions.append(faction)
            result = "requires factions { %s, }" % ", ".join(clearedFactions)
        elif len(myBuildingChain.Ownership) == len(Get.AllFactions()):
            result = ""
        else:
            result = "requires factions { %s, }" % ", ".join(myBuildingChain.Ownership)
        if result == "" and myBuildingChain.ExclusiveTag is not None:
            result = "requires no_other_%s" % myBuildingChain.ExclusiveTag
        elif not result == "" and myBuildingChain.ExclusiveTag is not None:
            result = "%s and no_other_%s" % (result, myBuildingChain.ExclusiveTag)
        if result == "" and self.RequiresBuilding is not None:
            result = f"requires building_present_min_level {Get.BuildingById(self.RequiresBuilding).BuildingChain} {self.RequiresBuilding}"
        elif result != "" and self.RequiresBuilding is not None:
            result = f"{result} and building_present_min_level {Get.BuildingById(self.RequiresBuilding).BuildingChain} {self.RequiresBuilding}"
        if result == "" and len(myBuildingChain.RequiresResources) > 0:
            resources = " or ".join([f"resource {r}" for r in myBuildingChain.RequiresResources])
            result = f"requires {resources}"
        elif not result == "" and len(myBuildingChain.RequiresResources) > 0:
            resources = " or ".join([f"resource {r}" for r in myBuildingChain.RequiresResources])
            result = f"{result} and {resources}"
        result = "requires is_player" if myBuildingChain.PlayerOnly else result
        if result == "" and myBuildingChain.AiOnly:
            result = "requires not is_player"
        elif result != "" and myBuildingChain.AiOnly:
            result = f"{result} and not is_player"
        return result

    def toDescrStratBuildingEntry(self):
        return "building\n\t{\n\t\ttype %s %s\n\t}\n" % (self.BuildingChain, self.Id)

    def getNameEvaluated(self, faction):
        if self.Name.count("%") == 2:
            aspect = self.Name.split("%")[1]
            religion = Get.ReligionByFaction(faction)
            return self.Name.replace(f"%{aspect}%", religion.getGodNameByReference(aspect))
        return self.Name