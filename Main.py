from singletons.World import World
from singletons.WorldMap import WorldMap
from singletons.Settings import Settings
import singletons.Get as Get
import singletons.Scripter as Scripter
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import ExcelLoader
import Globals
import FileGenerator
import Log
import OStools

mf = Globals.PathRootMod
Log.ErrorIf(not mf.is_dir(), f"{mf} not found! Edit PathRootMod in Globals.py file and/or create folder (modname/data)!")

Log.Info("Loading World")
Settings.load(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Setting"))
World.loadNames(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Name"))
World.loadSettlementLevels(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "SettlementLevel"))
World.loadCultures(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Culture"))
World.loadReligions(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Religion"))
World.loadFactions(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Faction"))
World.loadUnits(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Unit"))
World.loadBuildingChains(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "BuildingChain"))
World.loadBuildings(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Building"))
World.loadResources(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Resource"))
World.loadRebelFactions(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "RebelFaction"))
World.loadRegions(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Region"))
World.loadMounts(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Mount"))
World.loadLandmarks(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "Landmark"))
World.loadMercPools(ExcelLoader.getObjectsListFromExcel(Globals.FileConfig, "MercPool"))

World.checkLoad()

WorldMap.init()
World.init()
World.addSpecials()

OStools.CleanDir(f"text/")
OStools.RemoveFromModfolder(f"world/maps/base/map.rwm")
OStools.RemoveFromModfolder(f"world/maps/base/heights.hgt")
OStools.RemoveFromModfolder(f"world/maps/base/campaign/imperial_campaign/script.txt")
FileGenerator.generateFiles(locals())
FileGenerator.deployFiles()
FileGenerator.checkForMissingFiles()
FileGenerator.generateScriptTxt()

World.runChecks()
World.evaluate()

Log.Info("Finished - Version %s" % Get.Setting("Version"))

Log.Info("Known issues and solutions:")
Log.Info("Crash before battle map with new factions -> run game once with snd_save_events parameter")
Log.Info("Cant start campaign, goes back to menu -> city and/or character is placed on water")
Log.Info("Cant start campaign, goes back to menu -> faction present in descr_strat.txt which is missing in playable/unplayable/unlockable section")
