import Convert


class Mount:

    _UIDPrefix = "MO"  # Must be unique across all classes!

    def __init__(self, uid, id, name, effect):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        self.Id = Convert.Str(id)
        self.Name = Convert.Str(name)
        self.Effect = Convert.Str(effect)

    def __str__(self):
        return self.Name
