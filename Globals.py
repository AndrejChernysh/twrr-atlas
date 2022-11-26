
import pathlib

r"""
ENTER YOUR MODS DATA FOLDER BELOW - EXAMPLE r"C:\Users\yourusername\AppData\Local\Feral Interactive\Total War ROME REMASTERED\Mods\Local Mods\twrr\data"
"""
PathRootMod = pathlib.Path(  # WARNING -> That folders content will be overwritten - make sure to make a copy of it!
    r"C:\Users\andre\AppData\Local\Feral Interactive\Total War ROME REMASTERED\Mods\Local Mods\twrr\data"
)

PathRootLauncher = pathlib.Path(__file__).parent.resolve()
FileConfig = PathRootLauncher / "Configuration.xlsx"
PathMapsBase = PathRootMod / "world" / "maps" / "base"
PathModMapsCampaign = PathRootMod / "world" / "maps" / "campaign" / "imperial_campaign"
