import math

import Globals
import Log
import Stringtools
import singletons.Get as Get
from openpyxl import load_workbook


def factionOrCultureListTranslateToFactionList(factionOrCultureList: list[str]) -> list[str]:
    if factionOrCultureList is None:
        return None
    allTranslated = []
    for factionOrCulture in Stringtools.delimitedStringToList(factionOrCultureList):
        if Stringtools.isFactionId(factionOrCulture):
            allTranslated.append(factionOrCulture)
            continue
        translated = translateCultureToFactionsList(factionOrCulture)
        allTranslated.extend(translated)
    if "slave" in allTranslated:  # Slave should be always last in ownership list - all elements after it will be inactive
        allTranslated.remove("slave")
        allTranslated.append("slave")
    return allTranslated


def listTranslateCultureToFaction(listToTranslate):
    return [translateCultureToFactionsCommaDelimited(e) for e in listToTranslate]


def translateCultureToFactionsList(factionOrCulture: str):
    if factionOrCulture in Get.AllFactionIds():
        return [factionOrCulture]
    cultureFactionsMap = {}
    if factionOrCulture == "all":
        return Get.AllFactionIds()
    for faction in Get.AllFactions():
        if len(cultureFactionsMap) == 0 or faction.Culture not in cultureFactionsMap.keys():
            cultureFactionsMap[faction.Culture] = [faction.Id]
        else:
            currentFactions = cultureFactionsMap[faction.Culture]
            if len(currentFactions) == 0 or faction.Id not in currentFactions:
                currentFactions.append(faction.Id)
                cultureFactionsMap[faction.Culture] = currentFactions
    try:
        return cultureFactionsMap[factionOrCulture]
    except KeyError:
        Log.Error("Unknown faction referenced in Configuration.xlsx: %s" % factionOrCulture)


def translateCultureToFactionsCommaDelimited(culture):
    cultureFactionsMap = {}
    for faction in Get.AllFactions():
        if len(cultureFactionsMap) == 0 or faction.Culture not in cultureFactionsMap.keys():
            cultureFactionsMap[faction.Culture] = [faction.Id]
        else:
            currentFactions = cultureFactionsMap[faction.Culture]
            if len(currentFactions) == 0 or faction.Id not in currentFactions:
                currentFactions.append(faction.Id)
                cultureFactionsMap[faction.Culture] = currentFactions
    return ", ".join(cultureFactionsMap[culture])


def EffectToLabel(effectAndBonus: str):
    effect, bonus = effectAndBonus.split(" ")
    if effect == "Command":
        return f"+{bonus} command"
    elif effect == "Construction":
        return f"-{bonus}% construction cost"
    elif effect == "Influence":
        return f"+{bonus} influence"
    elif effect == "Management":
        return f"+{bonus} management"
    elif effect == "LineOfSight":
        return f"+{int(bonus)*0.5}% line of sight"
    elif effect == "MovementPoints":
        return f"+{bonus} movement points"
    else:
        exit(f"Could not translate effect and bonus: {effectAndBonus}")
        return effectAndBonus


def IndexToExpectedBannersTgaFile(index: int):
    number = 1 if index == 0 else math.ceil(index / 4)
    number = "0%s" % number if number < 10 else number  # 01 instead of 1 to ensure sorting
    filename = "symbols%s.tga.dds" % number
    return Globals.PathRootMod / "banners" / filename
