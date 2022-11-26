import Convert
import Stringtools


class RebelFaction:

    _UIDPrefix = "RF"  # Must be unique across all classes!

    def __init__(self, uid, id, name, category, chance, units, subfactionid):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.Category = Convert.Str(category)
        self.Chance = Convert.Int(chance)
        self.Units = Stringtools.delimitedStringToList(units, ",")
        self.SubfactionId = subfactionid

    def __str__(self):
        return self.Id
