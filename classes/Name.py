import Log


class Name:

    _UIDPrefix = "NA"  # Must be unique across all classes!

    def __init__(self, uid, cultureid, type, name):
        self.UID: str = f"{self._UIDPrefix}{uid}"
        Log.ErrorIf(cultureid is None, f"Name {uid} has no Culture")
        Log.ErrorIf(type is None, f"Name {uid} has no Type")
        Log.ErrorIf(name is None, f"Name {uid} has no Name")
        self.Culture: str = cultureid
        self.Type: str = type
        self.Text: str = name
        self.Id: str = name.replace(" ", "_")

    def __str__(self):
        return self.Id

    def __eq__(self, other):
        return self.UID == other.UID
