
import Enums
import Log
import Convert
import Translatetools
import singletons.Get as Get


class Culture:

    _UIDPrefix = "CU"  # Must be unique across all classes!

    def __init__(self, uid, id, name, ethnicity, maxSettlementLvl, smnamedcharacter, bmnamedcharacter, smgeneral, bmgeneral, uigroup: str, uigroupbuildings: str, iscivilized: bool, costtower: int, costfort: int, costspy: int, costassassin: int, costdiplomat: int, costmerchant: int, canhorde: bool, traitbonus: str):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        Log.ErrorIf(id is None, f"Culture {uid} has no ID")
        Log.ErrorIf(name is None, f"Culture {id} has no Name")
        Log.ErrorIf(ethnicity is None, f"Culture {id} has no Ethnicity")
        Log.ErrorIf(maxSettlementLvl is None, f"Culture {id} has no MaxCityLvl")
        Log.ErrorIf(smnamedcharacter is None, f"Culture {id} has no SMNamedCharacter")
        Log.ErrorIf(bmnamedcharacter is None, f"Culture {id} has no BMNamedCharacter")
        Log.ErrorIf(smgeneral is None, f"Culture {id} has no SMGeneral")
        Log.ErrorIf(bmgeneral is None, f"Culture {id} has no BMGeneral")
        Log.ErrorIf(uigroup is None, f"Culture {id} has no UIGroup")
        Log.ErrorIf(uigroupbuildings is None, f"Culture {id} has no UIGroupBuildings")
        Log.ErrorIf(iscivilized is None, f"Culture {id} has no IsCivilized")
        Log.ErrorIf(costtower is None, f"Culture {id} has no CostTower")
        Log.ErrorIf(costfort is None, f"Culture {id} has no CostFort")
        Log.ErrorIf(costspy is None, f"Culture {id} has no CostSpy")
        Log.ErrorIf(costassassin is None, f"Culture {id} has no CostAssassin")
        Log.ErrorIf(costdiplomat is None, f"Culture {id} has no CostDiplomat")
        Log.ErrorIf(costmerchant is None, f"Culture {id} has no CostMerchant")
        Log.ErrorIf(canhorde is None, f"Culture {id} has no CanHorde")
        Log.ErrorIf(traitbonus is None, f"Culture {id} has no TraitBonus")
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.Ethnicity = Convert.Str(ethnicity)
        assert self.Ethnicity in Enums.FACTION_ETHNICITIES, "%s ethnicity %s <> %s" % (self.Id, self.Ethnicity, Enums.FACTION_ETHNICITIES)
        self.MaxSettlementLvl = Convert.Int(maxSettlementLvl)
        self.SMNamedCharacter = Convert.Str(smnamedcharacter)
        self.BMNamedCharacter = Convert.Str(bmnamedcharacter)
        self.SMGeneral = Convert.Str(smgeneral)
        self.BMGeneral = Convert.Str(bmgeneral)
        self.UIGroup: str = uigroup
        self.UIGroupBuildings: str = uigroupbuildings
        self.IsCivilized: bool = iscivilized
        self.CostTower: int = costtower
        self.CostFort: int = costfort
        self.CostSpy: int = costspy
        self.CostAssassin: int = costassassin
        self.CostDiplomat: int = costdiplomat
        self.CostMerchant: int = costmerchant
        self.BonusLabels: list[str] = []
        self.CanHorde: bool = canhorde
        self.TraitBonus: str = traitbonus
        if self.TraitBonus is not None:
            assert " " in self.TraitBonus, f"{self.TraitBonus} is missing bonus indicator - valid example: Command 1"
            assert self.TraitBonus.split(" ")[0] in Enums.TRAIT_EFFECTS, f"{self.TraitBonus} effect is invalid - valid effects: {Enums.TRAIT_EFFECTS}"
            self.BonusLabels.append(f"{Translatetools.EffectToLabel(self.TraitBonus)} for generals")

    def __str__(self):
        return self.Name

    def getNames(self, type="all"):
        assert type == "all" or type in list(set([n.Type for n in Get.AllNames()])), "Invalid Nametype %s" % type
        if type == "all":
            return [n for n in Get.AllNames() if n.Culture == self.Id]
        else:
            return [n for n in Get.AllNames() if n.Culture == self.Id if n.Type == type]

    def getDescrNamelistsEntries(self, type="all"):
        assert type == "all" or type in list(set([n.Type for n in Get.AllNames()])), "Invalid Nametype %s" % type
        return "\n\t\t".join(["\"%s\"," % n for n in self.getNames(type)])

    def getIsCivilizedLower(self):
        return "true" if self.IsCivilized else "false"

    def getMaxCityLvlId(self):
        return [l.Id for l in Get.AllSettlementLevels() if l.Level == self.MaxSettlementLvl][0]
