So I have been developing a mod for Total War: Rome Remastered (TWRR) for the past weeks and wanted to share a tool I developed specifically of that. Feel free to use and enhance it in any way shape or form, it is still an early version and far from finished, but I will also keep updating it.

I do not take any responsibility for anything related to this tool. All the tools source code (. py format) is shipped to you, so you can see exactly what it does. It deletes and regenerates TWRR data files in your modfolder (.tga, .dds, .txt, .json files).

What is Atlas?
Basically it is a Python program which changes the way you are modding Rome Remastered. You usually mod TWRR by touching the data files (most of them are in *.txt, *.json format). With Atlas, all Data is now inside a single Configuration.xlsx file organized in Tables (Units table with all units and so on...) and all *.tga and *.dds files are inside a new structure. Ok, not all Configuration and all *.tga and *.dds files as of right now, but I am getting there.

How does it work?
In a very simple way - the tool is reading data from the Configuration.xlsx file and the few subfolders which contain *.tga and *.dds files and generates the known *.txt and *.json files for you. It also distributes the *.tga and *.dds files into the right folders for you.

Can you provide a simple example?
Until now when you add a new faction, you have to create several files of the same faction logo in different sizes and styles (greyed out etc.). With Atlas, you have to place that logo a single time inside one folder and you are done. Resizing, restyling, renaming and placing in right folders is automated. Another example: You want to rename faction Sparta to Lakedaimon? Normally you have to change a lot of different files for that. With Atlas you change a single Name value "Sparta" to "Lakedaimon" and a single Attributive valie "spartan" to "lakonian" in the Factions sheet and you are done. Want to change a cities position? Just adapt the dot in the map_regions.tga and you are done. No need to enter coordinates in different files and so on, Atlas can calculate the position correctly and uses it for generation of files that need these coordinates.

What are the advantages of that?
Basically three things: Cleanness, error avoidance and speed due to removed redundancies and automation. You can for example create a new faction with all characters on the map, units, unit cards, descriptions and so on in just 30 seconds (if you just copy an already present faction and change the new factions name). Also, there are error checks which are proofreading your data and warning you if anything might go wrong. For example when you define a religion for a faction but you haven't defined the icon for that religion yet, Atlas will warn you about that. As of cleanness - all of information, you have to provide only one single time inside the Configuration.xlsx. For example, you no longer have to create text entries for "parthian spy", "partian diplomat", "parthian merchant" and so on. You just define the attribute "parthian" for faction "Parthia" and Atlas will create all the agent (and more) text entries for you. Also, Atlas randomizes campaign elements each time you execute it: For example, agents and resources are placed randomly on defined regions each and every time.

Wait, creating a new faction in under 30 seconds?
Yes, if you copy an existing faction. You just copy a line in the Factions sheet in Configuration.xlsx, rename the faction ID, place the faction logo inside the ui/faction_logos and assign the starting region in the Regions sheet as well as unit ownership in the Units sheet (just search and replace with your copied faction, e.g. replace ", sparta" with ", sparta, athens") and you are good to go - you start the game and the new faction is standing there with all the characters, units, regions. Atlas even creates family trees for all factions for you, but you still can define a fixed name for leaders and heirs, their age and their traits if you want. If you dont, they will get random names, ages and traits, but you still can define which ones can be get randomly.l and so on.

Why would I want to use *.xlsx for modding - what are you, a Microsoft shareholder?
Yes I am, but the reason for that is that Excel is a great tool for organizing data - and thats what basically the *.txt and *.json files in TWRR are. They just hold data in a very inefficient, redundant and fragmented way. In *.xlsx, you can play around with that data far easier and faster in regards of filtering, sorting, searching and so on. Data is organized in sheets which contain a single table, for example you have a Regions sheet where all region data is defined and you have a Units sheet where all unit data is defined and so on.

More INFOS see below

------------------------------
INSTALLATION GUIDE

1. Make sure that you have installed the latest Python version on your computer https://www.python.org/
2. Make sure that you have installed the latest pip version on your computer https://packaging.python.org/en/late...ling-packages/
3. Install Pillow python module (needed for image processing): WIN + R, cmd.exe and type "pip install pillow"
4. Install Pandas python module (needed for excel processing): WIN + R, cmd.exe and type "pip install pandas"
5. Install Quik python module (needed for template processing): WIN + R, cmd.exe and type "pip install quik"
6. Put the atlas folder anywhere you want, it does not matter
7. Change the PathRootMod variable inside atlas/Globals.py to your mod folders data folder (I strongly recommend to use it only with a fresh and empty mod folder, it will not work with your mod already in place because you first have to rebuild your data inside the Configuration.xlsx)
8. Execute run.bat - WARNING: Files in your mod folder will be deleted and recreated like for example all faction portraits, all faction logos, the files descr_strat.txt, export_descr_buildings.txt and many more. DO NOT USE IT FOR AN EXISTING MOD, USE IT FOR A NEW MOD FROM SCRATCH. If you want to port your existing mod to Atlas, you have to remodel all the mod data (factions, cultures, religions, buildings, units, ...) in Configuration.xlsx! If you don't do that but still apply Atlas to your existing mod, you will lose most or even all your mod data as it will get overwritten by the mod data that is defined in Configuration.xlsx!

--------------------------------

Are there any downsides of using this tool?
Two - firstly, it is far from finished which means that not all data is organized there yet. For example, the battle models are missing, you have to keep editing it the old way. And secondly, some stuff is automated but not yet configurable in the Configuration.xlsx. Say you add a faction - all of the factions starting regions will be filled with garrisons consisting of random units. You can configure how many units will be added and which ones but you can't yet define for example that city Athens will get w units of unit x and the city of Sparta will get y units of unit z.

What TWRR objects can I mod already with Atlas?
Factions, cultures, religions, names, regions, mercenary pools, resources, landmarks, settlement levels, units (but not battle models), mounts, building chains, buildings and some settings like start date.

What is the tool automating for you as a modder for example?
+ Generation of all .txt and .json files you see in the templates subfolder
+ Generation of all .tga and .dds files you place in the resources and ui subfolder: portraits, building cards and pictures, unit cards and pictures, captain banners, faction icons (you place them one single time there and Atlas does the rest)
+ Positions on map are calculated automatically, no need to specify for example city and port positions, resource positions, agent and character positions, ...
+ Religion distribution in regions


Will this tool be developed further?
Yes, I am improving it day by day and I will upload new versions of it. Feel free to use the code to improve it by yourself and upload too.

Is Atlas free?
Yes. You can donate to me in Bitcoin though if you feel that I saved you some of your valuable time: 38Bum1WZ3Ust3WTbAEeQgnqQfSYR7BpT5e - I will continue to work on the tool nonetheless, I don't care about making money, I just love modding.

How do I use it?
1. Make sure that you have installed the latest Python version on your computer
2. Put the atlas folder anywhere you want, it does not matter
3. Change the PathRootMod variable inside atlas/Globals.py to your mod folders data folder (I strongly recommend to use it only with a fresh and empty mod folder, it will not work with your mod already in place because you first have to rebuild your data inside the Configuration.xlsx)
4. Execute run.bat - WARNING: Files in your mod folder will be deleted and recreated like for example all faction portraits, all faction logos, the files descr_strat.txt, export_descr_buildings.txt and many more. DO NOT USE IT FOR AN EXISTING MOD, USE IT FOR A NEW MOD FROM SCRATCH.
