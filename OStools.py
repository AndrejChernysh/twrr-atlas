import glob
import os
import pathlib
import random
import shutil
import PIL
import Globals
import Log
import re


def getFilesize(filepath, unit="KB"):
    size = pathlib.Path(filepath).stat().st_size
    Log.ErrorIf(size < 100, "Generated %s is smaller than 100 Bytes" % filepath)
    if unit == "B":
        return round(size, 2)
    elif unit == "KB":
        return round(size / 1024, 2)
    elif unit == "MB":
        return round(size / 1024 / 1024, 2)
    elif unit == "GB":
        return round(size / 1024 / 1024 / 1024, 2)
    else:
        exit("getFilesize unit parameter must be B, KB, MB or GB but is: %s" % unit)


def createFileUTF16LEBOM(path, content):
    # Make sure that these two write operations are the only in the with statements otherwise some files will not
    # get encoded in UTF-16 LE BOM properly
    with open(path, 'wb') as f:
        f.write(b"\xAC\n")
        f.write(content)  # Missing folders will not be generated in order to prevent wrong placements
    text = path.read_text()
    path.write_text(text.replace("\r", "\r\n"), encoding="utf-16")
    Log.Info("Generated %s (%s KB)" % (path.name, getFilesize(path, "KB")))


def createFileUTF8(path, content):
    try:
        with open(path, 'wb') as f:
            f.write(content)  # Missing folders will not be generated in order to prevent wrong placements
            path.write_text(path.read_text().replace("\r", "\r\n"))
    except FileNotFoundError:
        Log.Error(f"File {path} does not exist in modfolder. Add it manually if you placed source template correctly.")
    with open(path, 'rb') as open_file:
        content = open_file.read()
    content = content.replace(b"\r", b"|")
    content = content.replace(b"\n", b"|")
    content = content.replace(b"||", b"|")
    content = content.replace(b"|", b"\r\n")
    with open(path, 'wb') as open_file:
        open_file.write(content)
    Log.Info("Generated %s (%s KB)" % (path.name, getFilesize(path, "KB")))


def CleanDir(relativePathModFolder, fileNamePattern="*"):
    folder = pathlib.Path(Globals.PathRootMod / relativePathModFolder)
    for file in glob.glob(f"{folder}/*{fileNamePattern}"):
        try:
            os.remove(file)
        except WindowsError:
            pass


def ChooseFile(relativePathRootLauncherFolder):
    folder = pathlib.Path(Globals.PathRootLauncher / relativePathRootLauncherFolder)
    files = []
    for file in glob.glob(f"{folder}/*"):
        try:
            files.append(file)
        except WindowsError:
            pass
    Log.ErrorIf(len(files) == 0, f"No files for ChooseFile found in {folder}")
    return random.choice(files)


def Deploy(relativePathLauncherFolder, relativePathModFolder, WarnIfMissing=False):
    src = pathlib.Path(Globals.PathRootLauncher / relativePathLauncherFolder)
    dest = pathlib.Path(Globals.PathRootMod / relativePathModFolder)
    flag = dest.parent.resolve() / "#TheseFilesAreGeneratedByLauncherDoNotEditThem.info"
    if not flag.is_file():
        try:
            open(flag, 'a')
        except FileNotFoundError:
            Log.Error(f"Could not deploy flagfile, probably due to missing target subfolder in mod folder: {flag}")
    try:
        shutil.copyfile(src, dest)
    except FileNotFoundError:
        Log.WarnIf(WarnIfMissing, f"Missing file {src}")


def InLauncherFolder(relativePathLauncherFolder, warnIfMissing=False):
    filepath = pathlib.Path(Globals.PathRootLauncher / relativePathLauncherFolder)
    Log.WarnIf(warnIfMissing and not filepath.exists(), f"Missing {filepath}")
    return filepath.exists()


def InModFolder(relativePathModFolder):
    filepath = pathlib.Path(Globals.PathRootMod / relativePathModFolder)
    return filepath.exists()


def ListFilenamesModFolder(relativePathModFolder):
    path = pathlib.Path(Globals.PathRootMod / relativePathModFolder)
    path.mkdir(parents=True, exist_ok=True)
    test = [p.name for p in path.iterdir() if p.is_file()]
    return test


def RemoveFromModfolder(relativePathModFolderFileToDelete):
    path = pathlib.Path(Globals.PathRootMod / relativePathModFolderFileToDelete)
    try:
        path.unlink()
    except FileNotFoundError:
        Log.Info(f"Could not delete {path} because it does not exist.")


def getImgSize(fullpath, widthOrHeight):
    if widthOrHeight == "width":
        return PIL.Image.open(fullpath).width
    elif widthOrHeight == "height":
        return PIL.Image.open(fullpath).height
    else:
        Log.Error(f"Invalid parameter getImgSize: must be width or height but is {widthOrHeight}")


def countPixelByRGB(fullpath, r, g, b):
    return len([p for p in PIL.Image.open(fullpath).getdata() if p == (r, g, b)])

def ListFilesInModfolder(relativePathModFolderWithFilePattern: str):
    files = []
    folder = "/".join(relativePathModFolderWithFilePattern.split("/")[:-1])
    filepattern = relativePathModFolderWithFilePattern.split("/")[-1]
    filepattern = filepattern.replace("*", "\w+")
    path = Globals.PathRootMod / folder
    for file in os.listdir(path):
        if re.match(filepattern.lower(), file.lower()):
            files.append("\"data/" + folder + "/" + file + "\"")
    return ",\n".join(files)
