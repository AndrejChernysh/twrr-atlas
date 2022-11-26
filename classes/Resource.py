import Enums
import Convert
import Stringtools


class Resource:

    _UIDPrefix = "RS"  # Must be unique across all classes!

    def __init__(self, uid, id, name, value, type, tooltip, tooltipmining, tier, groups, modelmine, modeldefault, modelq1, modelq2, growthmodifier, isdepletable, baseturns, popimpact, depositcap, resourcepools):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.Value = Convert.Int(value)
        self.Type: str = str(type)
        assert self.Type in Enums.RESOURCE_TYPES, "Resource %s has invalid resource type" % self.Id
        self.Tooltip = Convert.Str(tooltip)
        self.TooltipMining = "TODO" if tooltipmining is None else Convert.Str(tooltipmining)
        self.Tier = Convert.Int(tier)
        self.Groups = Convert.ListFromCommaDelimitedString(groups)
        self.ModelMine = Convert.Str(modelmine)
        self.ModelDefault = Convert.Str(modeldefault)
        self.ModelQ1 = Convert.Str(modelq1)
        self.ModelQ2 = Convert.Str(modelq2)
        self.GrowthModifier = Convert.Int(growthmodifier)
        self.IsDepletable: bool = bool(isdepletable)
        self.BaseTurns = Convert.Int(baseturns)
        self.PopImpact = Convert.Int(popimpact)
        self.DepositCap: int = 0 if depositcap is None else Stringtools.intWithPossibleRange(depositcap)
        self.ResourcePools: list[str] = Stringtools.delimitedStringToList(resourcepools)
        self.IsOnMap: bool = self.Value is not None and self.Type not in ["slaves", "hidden"]
        self.IsHidden: bool = self.Type == "hidden"

    def __str__(self):
        return self.Name

    def __eq__(self, other):
        return self.Id == other.Id

    def getDescrSMResourceEntries(self):
        code = [f"\"subtype\": \"{self.Type}\","]
        if self.IsDepletable:
            code.append(f"\"depletable\": true,")
        code.append(f"\"name\": \"SMT_RESOURCE_{self.Id.upper()}\",")
        code.append(f"\"tooltip\": \"TMT_{self.Id.upper()}_TOOLTIP\",")
        code.append(f"\"icon\": \"data/ui/resources/resource_{self.Id}.tga\",")
        code.append(f"\"mining tooltip\": \"TMT_{self.Id.upper()}_MINE_TOOLTIP\",")
        if self.Tier is not None:
            code.append(f"\"tier\": {self.Tier},")
        if self.Value is not None:
            code.append(f"\"trade value\": {self.Value},")
        if self.GrowthModifier is not None:
            code.append(f"\"growth modifier\": {self.GrowthModifier},")
        if self.BaseTurns is not None:
            code.append(f"\"base turns\": {self.BaseTurns},")
        if self.PopImpact is not None:
            code.append(f"\"pop impact\": {self.PopImpact},")
        tags = "".join([f"\"{g}\", " for g in self.Groups])
        code.append(f"\"tags\": [ {tags} ],")
        if self.ModelMine is not None:
            code.append(f"\"mine model\": \"data/models_strat/{self.ModelMine}\",")
        qmodels = []
        if self.ModelQ1 is not None:
            qmodels.append(self.ModelQ1)
        if self.ModelQ2 is not None:
            qmodels.append(self.ModelQ2)
        qmodelsstr = "\n\t\t\t".join([f"\"data/models_strat/{f}\": {i+1}," for i, f in enumerate(qmodels)])
        code.append(f"\"quantity models\": {{ {qmodelsstr} }},")
        code.append(f"\"default model\": \"data/models_strat/{self.ModelDefault}\",")
        return "\n\t\t".join(code)
