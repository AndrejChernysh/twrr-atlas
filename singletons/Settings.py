import Log


class Settings(object):
    Settings = None

    @classmethod
    def load(cls, settings):
        cls.Settings = settings
        Log.Info("Initialized %s settings" % len(cls.Settings))

    @classmethod
    def get(cls, setting):
        try:
            result = [s.Value for s in cls.Settings if s.Setting == setting][0]
        except IndexError:
            result = None
            Log.Error(f"Setting not in Configuration.xlsx: {setting}")
        if result.lower() == "true":
            return True
        if result.lower() == "false":
            return False
        if result.isdigit():
            return int(result)
        if all([c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."] for c in result]):
            if result.endswith(".0"):
                return int(round(float(result)))
            return float(result)
        return str(result)
