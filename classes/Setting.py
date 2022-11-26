import Convert


class Setting:

    _UIDPrefix = "SE"  # Must be unique across all classes!

    def __init__(self, uid, setting, value, remark):
        self.UID = "%s%s" % (self._UIDPrefix, uid)
        self.Setting = Convert.Str(setting)
        self.Value = Convert.Str(value)
        self.Remark = Convert.Str(remark)

    def __str__(self):
        return "%s (%s)" % (self.Setting, self.Value)
