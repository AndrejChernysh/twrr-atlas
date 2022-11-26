import Convert
from classes.Position import Position
import singletons.Get as Get


class Tile:

    _UIDPrefix = "TI"  # Must be unique across all classes!

    def __init__(self, x: int, y: int, regionid: str, iscity: bool, isport: bool, issea: bool, groundtype: str, feature: str):
        self.UID = "%sX%sY%s" % (self._UIDPrefix, x, y)
        self.X = Convert.Int(x)
        self.Y = Convert.Int(y)
        self.RegionId = regionid
        self.IsCity = iscity
        self.IsPort = isport
        self.GroundType = groundtype
        self.Feature = feature
        self.IsRiver = feature in ["River", "RiverOrigin"]
        self.IsMountain = groundtype in ["MountainsHigh", "MountainsLow"]
        self.IsForestDense = groundtype == "ForestDense"
        self.IsVolcano = feature == "Volcano"
        self.IsSea = issea
        self.IsLandmark = bool([l for l in Get.AllLandmarks() if l.Position.X == x and l.Position.Y == y])
        self.IsAccessible = not (self.IsForestDense or issea or iscity or self.IsVolcano or self.IsRiver or
                                 self.IsMountain or self.IsLandmark)

    def __str__(self):
        return "%s, %s" % (self.X, self.Y)

    def toPosition(self):
        return Position(self.X, self.Y)

    def __eq__(self, other):
        return self.X * 10000 + self.Y == other.X * 10000 + other.Y
