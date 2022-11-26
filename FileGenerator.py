import Convert
import Enums
import Log
import quik
import pathlib
import Globals
import OStools
import os
import Translatetools
import singletons.Get as Get
from pathlib import Path


def generateFiles(locals):
    Log.Info("Generating Files")
    for path, subdirs, files in os.walk(Globals.PathRootLauncher / "templates"):
        subdirs.sort(reverse=True)
        for name in files:
            templatePath = pathlib.Path(path) / name
            subpath = path.replace(str(Globals.PathRootLauncher / "templates"), "")
            subpath = subpath[1:] if subpath.startswith("\\") else subpath
            targetFile = Globals.PathRootMod / subpath / name
            Path(Globals.PathRootMod / subpath).mkdir(parents=True, exist_ok=True)
            Path(targetFile).touch(exist_ok=True)
            loader = quik.FileLoader('txt')
            Log.Info(f"Reading {templatePath}")
            loaderTemplate = loader.load_template(templatePath)
            code = loaderTemplate.render(locals, loader=quik.FileLoader('txt')).encode('utf-8')
            Log.WarnIf(str(code).count("@") > 0, "Generated %s contains @ - possible template error" % targetFile)
            if subpath.startswith("text"):
                OStools.createFileUTF16LEBOM(targetFile, code)
            else:
                OStools.createFileUTF8(targetFile, code)


def deployFiles():
    if not Get.Setting("SkipFileDeployment"):
        Log.Info("Cleaning Directories")
        OStools.CleanDir("ui/captain banners/")
        OStools.CleanDir("ui/captain banners/dead/")
        OStools.CleanDir("textures/battleStandards")
        OStools.CleanDir("ui/faction_icons")
        OStools.CleanDir("menu/symbols/fe_buttons_feral")
        OStools.CleanDir(f"world/maps/campaign/imperial_campaign", "leader_pic_*.tga")
        for culture in Get.AllCultures():
            OStools.CleanDir(f"ui/{culture.Id}/buildings/")
            OStools.CleanDir(f"ui/{culture.Id}/eventpics/")
            OStools.CleanDir(f"ui/{culture.Id}/buildings/construction/")
        Log.Info("Deploying Files")
        for faction in Get.AllFactions():
            for subdir in ["units", "units_classic"]:
                if not OStools.InModFolder(f"ui/{subdir}/{faction.Id}/"):
                    os.mkdir(pathlib.Path(Globals.PathRootMod / f"ui/{subdir}/{faction.Id}/"))
                OStools.CleanDir(f"ui/{subdir}/{faction.Id}/")
                for agent in Enums.AGENTS:
                    agentCard = f"ui/unitCards/{agent}_{faction.TextureCode}.tga"
                    Log.WarnIfNot(OStools.InLauncherFolder(agentCard), f"Missing: {agentCard}")
                    OStools.Deploy(agentCard, f"ui/{subdir}/{faction.Id}/{agent}.tga")  # Filename does not start with hashtag for agents
                for unit in faction.getUnits():
                    if OStools.InLauncherFolder(f"ui/unitCards/{unit.Dictionary}_{faction.TextureCode}.tga"):
                        OStools.Deploy(f"ui/unitCards/{unit.Dictionary}_{faction.TextureCode}.tga", f"ui/{subdir}/{faction.Id}/#{unit.Dictionary}.tga")
                    else:
                        Log.Warn(f"Missing file in launcher folder: ui/unitCards/{unit.Dictionary}_{faction.TextureCode}.tga")
                        OStools.Deploy(f"ui/unitCards/{unit.Dictionary}.tga", f"ui/{subdir}/{faction.Id}/#{unit.Dictionary}.tga")
            OStools.Deploy(OStools.ChooseFile(f"resources/portraits_young/{faction.getCulture().UIGroup}/"),
                           f"ui/captain banners/captain_portrait_{faction.Id}.tga")
            OStools.Deploy(OStools.ChooseFile(f"resources/portraits_young/{faction.getCulture().UIGroup}/"),
                           f"ui/captain banners/captain_portrait_{faction.Id}_rebel.tga")
            OStools.Deploy(OStools.ChooseFile(f"resources/portraits_young/{faction.getCulture().UIGroup}/"),
                           f"ui/captain banners/captain_card_{faction.Id}.tga")
            OStools.Deploy(OStools.ChooseFile(f"resources/portraits_young/{faction.getCulture().UIGroup}/"),
                           f"ui/captain banners/captain_card_{faction.Id}_rebel.tga")
            OStools.Deploy(OStools.ChooseFile(f"resources/portraits_young/{faction.getCulture().UIGroup}/"),
                           f"ui/captain banners/dead/captain_card_{faction.Id}.tga")
            Convert.ImageToGrey(Globals.PathRootMod / f"ui/captain banners/dead/captain_card_{faction.Id}.tga")
            oldYoung = "old" if faction.LeaderAge is None or faction.LeaderAge > 40 else "young"
            OStools.Deploy(OStools.ChooseFile(f"resources/portraits_{oldYoung}/{faction.getCulture().UIGroup}/"),
                           f"world/maps/campaign/imperial_campaign/leader_pic_{faction.Id}.tga")
            OStools.CleanDir(f"world/maps/campaign/imperial_campaign", f"map_{faction.Id}.tga")
            OStools.Deploy(f"resources/map_dummy.tga", f"world/maps/campaign/imperial_campaign/map_{faction.Id}.tga")
            logo = Globals.PathRootLauncher / f"ui/factionIcons/{faction.Id}.tga"
            Log.ErrorIfNoFile(logo)
            Log.ErrorIf(OStools.getImgSize(logo, "width") != 512 or OStools.getImgSize(logo, "height") != 512, f"{logo} must be 512x512px")
            OStools.Deploy(logo, f"ui/faction_icons/{faction.Id}.tga")
            Convert.ImageResize(Globals.PathRootMod / f"ui/faction_icons/{faction.Id}.tga", 320, 320)
            for suffix in ["", "_grey", "_roll", "_select"]:
                OStools.Deploy(logo, f"menu/symbols/fe_buttons_feral/symbol128_{faction.Id}{suffix}.tga")
            Convert.ImageToGrey(Globals.PathRootMod / f"menu/symbols/fe_buttons_feral/symbol128_{faction.Id}_grey.tga")
            Convert.ImageBrighten(Globals.PathRootMod / f"menu/symbols/fe_buttons_feral/symbol128_{faction.Id}_select.tga")
            standard = Globals.PathRootLauncher / f"ui/factionStandards/{faction.Id}.tga.dds"
            OStools.Deploy(standard, f"textures/battleStandards/{faction.Id}.tga.dds", True)
            Log.Info(f"Deployed files for faction {faction.Id}")
        for filename in os.listdir(Globals.PathRootLauncher / "ui" / "eventPics"):
            eventpic = Globals.PathRootLauncher / "ui" / "eventPics" / filename
            if os.path.isfile(eventpic):
                for culture in Get.AllCultures():
                    OStools.Deploy(eventpic, f"ui/{culture.Id}/eventpics/{filename}")
        for culture in Get.AllCultures():
            for building in Get.AllBuildings():
                card = f"ui/buildingCards/dummy.tga"
                warnIfMissing = True
                if OStools.InLauncherFolder(f"ui/buildingCards/{building.BuildingChain}{building.Level}.tga"):
                    card = f"ui/buildingCards/{building.BuildingChain}{building.Level}.tga"
                    warnIfMissing = False
                if OStools.InLauncherFolder(f"ui/buildingCards/{culture.UIGroupBuildings}/{building.BuildingChain}{building.Level}.tga", warnIfMissing):
                    card = f"ui/buildingCards/{culture.UIGroupBuildings}/{building.BuildingChain}{building.Level}.tga"
                OStools.Deploy(card, f"ui/{culture.Id}/buildings/#{culture.Id}_{building.Id}.tga")
                OStools.Deploy(card, f"ui/{culture.Id}/buildings/construction/#{culture.Id}_{building.Id}.tga")
                if OStools.getImgSize(Globals.PathRootMod / f"ui/{culture.Id}/buildings/#{culture.Id}_{building.Id}.tga", "width") != 156:
                    Convert.ImageResize(Globals.PathRootMod / f"ui/{culture.Id}/buildings/#{culture.Id}_{building.Id}.tga", 156, 124)
                Convert.ImageResize(Globals.PathRootMod / f"ui/{culture.Id}/buildings/construction/#{culture.Id}_{building.Id}.tga", 128, 102)
            for filename in os.listdir(Globals.PathRootLauncher / "ui" / "eventPics" / culture.Id):
                eventpic = Globals.PathRootLauncher / "ui" / "eventPics" / culture.Id / filename
                OStools.Deploy(eventpic, f"ui/{culture.Id}/eventpics/{filename}")
            Log.Info(f"Deployed files for culture {culture.Id}")
    else:
        Log.Warn("Skipped file deployment (set SkipFileDeployment to FALSE in Configuration.xlsx) - do not skip if you add/change factions/units")


def checkForMissingFiles():
    Log.Info("Checking if there are any missing files")
    Log.WarnIfNoFile(Globals.PathRootMod / "pips", f"settlementdetails.tga")
    for file in Enums.WORLDMAPSBASE_MANDATORY_FILES:
        Log.WarnIfNoFile(Globals.PathRootMod / "world" / "maps" / "base", file)
    for religion in Get.AllReligions():
        Log.WarnIfNoFile(Globals.PathRootMod / "pips", f"{religion.Id}.tga")
        Log.WarnIfNoFile(Globals.PathRootMod / "pips", f"{religion.Id}_unrest.tga")
    for faction in Get.AllFactions():
        culture = Get.CultureById(faction.Culture)
        Log.WarnIfNoFile(Translatetools.IndexToExpectedBannersTgaFile(faction.Index))
        Log.WarnIfNoFile(Globals.PathRootMod / "ui" / "faction_icons", f"{faction.Id}.tga")
        for a in ["", "_grey", "_roll"]:
            Log.WarnIfNoFile(Globals.PathRootMod / "menu" / "symbols" / "fe_buttons_feral", f"symbol128_{faction.Id}{a}.tga")
        Log.WarnIfNoFile(Globals.PathRootMod / "ui" / "captain banners", f"captain_card_{faction.Id}.tga")
        Log.WarnIfNoFile(Globals.PathRootMod / "ui" / "captain banners", f"captain_card_{faction.Id}_rebel.tga")
        Log.WarnIfNoFile(Globals.PathRootMod / "ui" / "captain banners" / "dead", f"captain_card_{faction.Id}.tga")
        Log.WarnIfNoFile(Globals.PathRootMod / "characters" / "textures", f"{culture.SMGeneral}_{faction.TextureCode}.tga.dds")
        Log.WarnIfNoFile(Globals.PathRootMod / "characters" / "textures", f"{culture.SMNamedCharacter}_{faction.TextureCode}.tga.dds")
        for agent in Enums.AGENTS:
            Log.WarnIfNoFile(Globals.PathRootMod / "characters" / "textures", f"{agent}_{faction.TextureCode}.tga.dds")


def generateScriptTxt():
    if not bool(Get.Setting("SkipScriptGeneration")):
        Log.Info("Generating scripts - this may take some time...")
        folderCampaign = Globals.PathRootMod / "world" / "maps" / "campaign" / "imperial_campaign"
        folderSubscripts = folderCampaign / "subscripts"
        code = []
        counters = ["dummy_r", "dummy_f"]  # Needed for Scripter.MessageInfo()
        countersPersistent = []  # Needed for Scripter.MessageInfo()
        for subscript in os.listdir(folderSubscripts):
            countMonitors = 0
            with open(folderSubscripts / subscript, "r") as f:
                code.append(f"\n; {subscript} START\n")
                for line in f.readlines():
                    Log.ErrorIf("set_counter" in line and "=" in line, f"{subscript}: set_counter and = in one line. Remove the =")
                    code.append(line)
                    countMonitors += 1 if "monitor" in line else 0
                    for o in ["set_counter", "I_CompareCounter"]:
                        if o in line:
                            counter = line.split(o)[1].strip()
                            for x in [" ", ";"]:
                                if x in counter:
                                    counter = counter.split(x)[0]
                            if counter not in counters and "persistent" not in line and counter not in countersPersistent:
                                counters.append(counter)
                            if counter not in countersPersistent and "persistent" in line and counter not in counters:
                                countersPersistent.append(counter)
                code.append(f"\n; {subscript} END\n")
            countMonitors = round(countMonitors/2)
            Log.Info(f"Added subscript {subscript} to script ({OStools.getFilesize(folderSubscripts / subscript)} KB, {countMonitors} monitors)")
        script = folderCampaign / "script.txt"
        with open(script, "w") as f:
            f.write("\nscript\n")
            for counterPersistent in countersPersistent:
                f.write(f"declare_persistent_counter {counterPersistent}\n")
            for counter in counters:
                f.write(f"declare_counter {counter}\n")
            for line in code:
                f.write(line)
            f.write("\nend_script\n")
        Log.Info(f"Created script ({OStools.getFilesize(script)} KB)")
    else:
        Log.Warn("Skipped campaign script generation (set SkipScriptGeneration to FALSE in Configuration.xlsx)")
