import shutil
import os
import OStools
import subprocess
from pydub import AudioSegment

filepath = r"C:\Program Files (x86)\Steam\steamapps\common\Total War ROME REMASTERED\Contents\Resources\Data\data\world\maps\base\descr_regions.txt"

pos = 0
regionname = ""
cityname = ""
natives = ""
rebels = ""
rgb = ""
resources = ""
triumph = ""
fertility = ""
for l in open(filepath, "r"):
    l = l.strip()
    if not l.startswith(";") and not l.strip() == "":
        if pos == 0:
            regionname = l
        elif pos == 1:
            cityname = l
        elif pos == 2:
            natives = l
        elif pos == 3:
            rebels = l
        elif pos == 4:
            rgb = l
        elif pos == 5:
            resources = l
        elif pos == 6:
            triumph = l
        elif pos == 7:
            fertility = l
        pos += 1
        if pos == 8:
            pos = 0
            print(f"{regionname}\t{cityname}\t?\t?\t{natives}\t?\tBrigantes\t{rgb}")

exit()

types = ["cry", "fire", "flee", "idle", "signals"]
for type in types:
    path = f"C:\\Users\\andre\\AppData\\Local\\Feral Interactive\\Total War ROME REMASTERED\\Mods\\Local Mods\\twrr\\data\\sounds\\{type}\\"
    for file in os.listdir(path):
        print(file)
        song = AudioSegment.from_wav(path + file)
        song_10_db_louder = song + 10
        # save the output
        song_10_db_louder.export(path + file, "wav")
exit()

colors = [
"red"
,"white"
,"green"
,"brown"
,"blue"
,"yellow"
,"black"
,"orange"
,"grey"
,"purple"
]

dir = r"C:\\Users\\andre\\Desktop\\temp\\"


for i, file in enumerate(os.listdir(dir)):
    orgFile = file
    file = file.replace("#", "").replace(".tga", "")
    file = f"{file}_blue.tga"
    os.rename(dir+orgFile, dir+file)

exit()

for i, file in enumerate(os.listdir(dir)):
    os.rename(dir+file, dir+f"winter{i}.mp3")

for i, file in enumerate(os.listdir(dir)):
    newfilename = file.replace(".mp3", ".opus")
    os.system(f"cd {dir}")
    os.system(f"ffmpeg -i {dir+file} -c:a libopus {dir+newfilename}")
