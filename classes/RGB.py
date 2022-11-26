import Log


class RGB:

    def __init__(self, r: int, g: int, b: int):
        self.R: int = r
        self.G: int = g
        self.B: int = b

    def __str__(self):
        return str(self.R * 1000000 + self.G * 1000 + self.B).zfill(9)

    def __int__(self):
        return self.R * 1000000 + self.G * 1000 + self.B

    def toCommaDelimitedString(self):
        return f"{self.R}, {self.G}, {self.B}"

    def getFeature(self):
        if str(self) == "000000255":
            return "River"
        elif str(self) == "000255255":
            return "RiverCrossing"
        elif str(self) == "255255255":
            return "RiverOrigin"
        elif str(self) == "255255000":
            return "Cliff"
        elif str(self) == "255000000":
            return "Volcano"
        elif str(self) == "000000000":
            return "NoFeature"
        else:
            Log.Error("Unknown Feature RGB: %s" % self)

    def getGroundType(self):
        if str(self) == "000128128":
            return "FertileLow"
        elif str(self) == "096160064":
            return "FertileMedium"
        elif str(self) == "101124000":
            return "FertileHigh"
        elif str(self) == "000000000":
            return "Wilderness"
        elif str(self) == "196128128":
            return "MountainsHigh"
        elif str(self) == "098065065":
            return "MountainsLow"
        elif str(self) == "128128064":
            return "Hills"
        elif str(self) == "000064000":
            return "ForestDense"
        elif str(self) == "000128000":
            return "ForestSparse"
        elif str(self) == "000255128":
            return "Swamp"
        elif str(self) == "064000000":
            return "Ocean"
        elif str(self) == "128000000":
            return "SeaDeep"
        elif str(self) == "196000000":
            return "SeaShallow"
        elif str(self) == "255255255":
            return "Beach"
        else:
            Log.Error("Unknown GroundType RGB: %s" % self)
