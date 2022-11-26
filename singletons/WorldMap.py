import PIL
import Log
import Globals
from classes.Tile import Tile
from classes.RGB import RGB
import singletons.Get as Get


class WorldMap(object):
    Tiles: list[Tile] = []
    Width = 0
    Height = 0

    @classmethod
    def init(cls):
        for fileNamePart in ["regions", "features", "ground_types"]:
            Log.ErrorIfNoFile(Globals.PathMapsBase / f"map_{fileNamePart}.tga", addendumTxt="(is needed even if you want to use unmodified original)")
        mapRegionsTga = PIL.Image.open(Globals.PathMapsBase / "map_regions.tga")
        mapFeaturesTga = PIL.Image.open(Globals.PathMapsBase / "map_features.tga")
        mapGroundTypesTga = PIL.Image.open(Globals.PathMapsBase / "map_ground_types.tga")
        cls.Width = mapRegionsTga.width
        cls.Height = mapRegionsTga.height
        lastrgbc = -1
        lastRegion = None
        for x in range(0, cls.Width):
            for y in range(0, cls.Height):
                r, g, b = mapRegionsTga.getpixel((x, y))
                FeaturePixel = mapFeaturesTga.getpixel((x, y))
                FeatureRGB = RGB(FeaturePixel[0], FeaturePixel[1], FeaturePixel[2])
                GroundTypePixel1 = mapGroundTypesTga.getpixel((x*2, y*2))
                GroundTypePixel2 = mapGroundTypesTga.getpixel((x*2+1, y*2))
                GroundTypePixel3 = mapGroundTypesTga.getpixel((x*2, y*2+1))
                GroundTypePixel4 = mapGroundTypesTga.getpixel((x*2+1, y*2+1))
                GroundTypePixels = []
                for pixel in [GroundTypePixel1, GroundTypePixel2, GroundTypePixel3, GroundTypePixel4]:
                    GroundTypePixels.append(RGB(pixel[0], pixel[1], pixel[2]))
                GroundTypeRGB = max(GroundTypePixels, key=GroundTypePixels.count)
                if len([p for p in GroundTypePixels if "Mountains" in p.getGroundType()]) > 0:
                    GroundTypeRGB = RGB(98, 65, 65)  # MountainsLow
                elif len([p for p in GroundTypePixels if p.getGroundType() == "ForestDense"]) > 0:
                    GroundTypeRGB = RGB(0, 64, 0)  # ForestDense
                IsSingleGroundType = GroundTypePixel1 == GroundTypePixel2 == GroundTypePixel3 == GroundTypePixel4
                isSea = False
                if GroundTypeRGB in ["SeaDeep", "SeaShallow", "Ocean"] and IsSingleGroundType:
                    isSea = True
                inGameX = x
                inGameY = cls.Height - y - 1
                rgbc = r * 1000000 + g * 1000 + b
                isSameRGBAgain = rgbc == lastrgbc
                isCity = rgbc == 0
                isPort = rgbc == 255255255
                if isSameRGBAgain:
                    region = lastRegion
                elif not isCity and not isPort:
                    try:
                        region = Get.RegionByRGB(r, g, b)
                        isSea = False
                    except IndexError:
                        region = None
                        isSea = True
                    lastRegion = region
                else:
                    region = lastRegion
                    isSea = False
                try:
                    regionIdOrNone = None if region is None else region.IdRegion
                except AttributeError:
                    Log.Error(f"Cannot locate where settlement of {lastRegion} is - it is probably surrounded by too much water additionally to its own port - place the port or the city elsewhere!")
                if regionIdOrNone is None and not isSea:
                    if Get.RegionIdByTgaXY(x, y) is not None:
                        regionIdOrNone = Get.RegionIdByTgaXY(x, y)
                        lastRegion = regionIdOrNone
                cls.Tiles.append(Tile(inGameX, inGameY, regionIdOrNone, isCity, isPort, isSea, GroundTypeRGB.getGroundType(), FeatureRGB.getFeature()))
                if not isSameRGBAgain:
                    lastrgbc = rgbc
        Log.Info("Initialized %s tiles" % len(cls.Tiles))
