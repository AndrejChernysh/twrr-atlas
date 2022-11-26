import Convert
import Log


class Religion:

    _UIDPrefix = "RL"  # Must be unique across all classes!

    def __init__(self, uid, id, name, group, battlegod, farminggod, fertilitygod, fungod, healinggod, lawgod, lovegod, navalgod, one_godgod, tradegod, governmentgod, forgegod):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.Group = Convert.Str(group)
        self.BattleGod = Convert.Str(battlegod)
        self.FarmingGod = Convert.Str(farminggod)
        self.FertilityGod = Convert.Str(fertilitygod)
        self.FunGod = Convert.Str(fungod)
        self.HealingGod = Convert.Str(healinggod)
        self.LawGod = Convert.Str(lawgod)
        self.LoveGod = Convert.Str(lovegod)
        self.NavalGod = Convert.Str(navalgod)
        self.One_godGod = Convert.Str(one_godgod)
        self.TradeGod = Convert.Str(tradegod)
        self.GovernmentGod = Convert.Str(governmentgod)
        self.ForgeGod = Convert.Str(forgegod)

    def __str__(self):
        return self.Name

    def getGodNameByReference(self, reference):
        ref = reference.lower()
        if ref == "battlegod":
            return self.BattleGod
        elif ref == "farminggod":
            return self.FarmingGod
        elif ref == "fertilitygod":
            return self.FertilityGod
        elif ref == "fungod":
            return self.FunGod
        elif ref == "healinggod":
            return self.HealingGod
        elif ref == "lawgod":
            return self.LawGod
        elif ref == "lovegod":
            return self.LoveGod
        elif ref == "navalgod":
            return self.NavalGod
        elif ref == "one_godgod":
            return self.One_godGod
        elif ref == "tradegod":
            return self.TradeGod
        elif ref == "governmentgod":
            return self.GovernmentGod
        elif ref == "forgegod":
            return self.ForgeGod
        else:
            Log.Error("Could not translate reference {} to deity!")
