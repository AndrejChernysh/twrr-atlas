import shutil
import os
import OStools
import subprocess
from pydub import AudioSegment

filepath = r"C:\Program Files (x86)\Steam\steamapps\common\Total War ROME REMASTERED\Contents\Resources\Data\data\export_descr_unit.txt"

with open(filepath, "r") as f:
    lines = f.readlines()

if filepath.endswith("export_descr_unit.txt"):
    lines = [l.strip() for l in lines if not l.strip().startswith(";") and len(l.strip()) > 0]  # Remove comments and empty lines
    lines = [l.split(";")[0].strip() if ";" in l else l for l in lines]  # Remove inline comments
    type = dictionary = category = uClass = voicetype = soldier = special = soldiers = extras = mass = mount = attributes = formation = hp = hpextras = ""
    statPri = statPriAttr = statSec = statSecAttr = statPriArmour = statSecArmour = statHeat = statGround = morale = discipline = training = chargeDist = ""
    costTurns = costTraining = costUpkeep = costUpgradeWpn = costUpgradeArmour = owners = ""
    for i, line in enumerate(lines):
        unitEntry = [type, dictionary, type.title(), category, uClass, voicetype, soldier, special, soldiers, extras, mass, mount, attributes, formation, hp, hpextras, statPri, statPriAttr,
                     statSec, statSecAttr, statPriArmour, statSecArmour, statHeat, statGround, morale, discipline, training, chargeDist, costTurns, costTraining, costUpkeep, costUpgradeWpn,
                     costUpgradeArmour, owners, "", "TODO"]
        if line.startswith("type"):
            if not line.replace("type", "", 1).strip() == type:
                print("\t".join([u.strip() for u in unitEntry]))  # Print entry because we are already processing a new unit
                type = dictionary = category = uClass = voicetype = soldier = special = soldiers = extras = mass = mount = attributes = formation = hp = hpextras = ""
                statPri = statPriAttr = statSec = statSecAttr = statPriArmour = statSecArmour = statHeat = statGround = morale = discipline = training = chargeDist = ""
                costTurns = costTraining = costUpkeep = costUpgradeWpn = costUpgradeArmour = owners = ""
            type = line.replace("type", "", 1).strip()
        if line.startswith("dictionary"):
            dictionary = line.replace("dictionary", "", 1).strip()
        if line.startswith("category"):
            category = line.replace("category", "", 1).strip()
        if line.startswith("class"):
            uClass = line.replace("class", "", 1).strip()
        if line.startswith("mount") and not line.startswith("mount_effect"):
            mount = line.replace("mount", "", 1).strip()
        if line.startswith("voice_type"):
            voicetype = line.replace("voice_type", "", 1).strip()
        if line.startswith("attributes"):
            attributes = line.replace("attributes", "", 1).strip()
        if line.startswith("formation"):
            formation = line.replace("formation", "", 1).strip()
        if line.startswith("stat_pri") and not line.startswith("stat_pri_"):
            statPri = line.replace("stat_pri", "", 1).strip()
        if line.startswith("stat_pri_attr"):
            statPriAttr = line.replace("stat_pri_attr", "", 1).strip()
        if line.startswith("stat_sec") and not line.startswith("stat_sec_"):
            statSec = line.replace("stat_sec", "", 1).strip()
        if line.startswith("stat_sec_attr"):
            statSecAttr = line.replace("stat_sec_attr", "", 1).strip()
        if line.startswith("stat_pri_armour"):
            statPriArmour = line.replace("stat_pri_armour", "", 1).strip()
        if line.startswith("stat_sec_armour"):
            statSecArmour = line.replace("stat_sec_armour", "", 1).strip()
        if line.startswith("stat_heat"):
            statHeat = line.replace("stat_heat", "", 1).strip()
        if line.startswith("stat_mental"):
            morale, discipline, training = line.replace("stat_mental", "", 1).strip().split(",")
        if line.startswith("stat_cost"):
            costTurns, costTraining, costUpkeep, costUpgradeWpn, costUpgradeArmour, costCustom = line.replace("stat_cost", "", 1).strip().split(",")
        if line.startswith("stat_charge_dist"):
            chargeDist = line.replace("stat_charge_dist", "", 1).strip()
        if line.startswith("stat_ground"):
            statGround = line.replace("stat_ground", "", 1).strip()
        if line.startswith("stat_health"):
            hp, hpextras = line.replace("stat_health", "", 1).strip().split(",")
        if line.startswith("soldier"):
            soldier, soldiers, extras, mass = line.replace("soldier", "", 1).strip().split(",")
        for specialtype in ["ship", "animal", "engine"]:
            if line.startswith(specialtype):
                special = "%s:%s" % (specialtype, line.replace(specialtype, "", 1).strip())
        if line.startswith("ownership"):
            owners = line.replace("ownership", "", 1).strip()
        if i + 1 == len(lines):
            unitEntry = [type, dictionary, type.title(), category, uClass, voicetype, soldier, special, soldiers, extras, mass, mount, attributes, formation, hp, hpextras, statPri, statPriAttr,
                         statSec, statSecAttr, statPriArmour, statSecArmour, statHeat, statGround, morale, discipline, training, chargeDist, costTurns, costTraining, costUpkeep, costUpgradeWpn,
                         costUpgradeArmour, owners, "", "TODO"]
            print("\t".join([u.strip() for u in unitEntry]))  # Print last entry if last line
else:
    exit("Undefined processing for file: %s" % filepath)
