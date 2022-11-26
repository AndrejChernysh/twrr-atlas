
import datetime
import pathlib
from typing import overload

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def Info(text):
    print("%s %s" % (datetime.datetime.now().strftime("%H:%M:%S:%f"), text))


def Warn(text):
    print(f"{WARNING}%s %s{ENDC}" % (datetime.datetime.now().strftime("%H:%M:%S:%f"), text))


def Error(text):
    exit(f"{FAIL}%s %s{ENDC}" % (datetime.datetime.now().strftime("%H:%M:%S:%f"), text))


def InfoIf(condition, text):
    if condition:
        Info(text)


def WarnIf(condition, text):
    if condition:
        Warn(text)


def WarnIfNot(condition, text):
    if not condition:
        Warn(text)


def ErrorIf(condition, text):
    if condition:
        Error(text)


def ErrorIfNot(condition, text):
    if not condition:
        Error(text)


def ErrorIfNoFile(folderOrFullpath: str, filename=None, addendumTxt="") -> None:
    if filename is not None:
        fullpath = pathlib.Path(folderOrFullpath) / filename
        if not fullpath.is_file():
            Error("Missing file %s %s" % (fullpath, addendumTxt))
    else:
        if not pathlib.Path(folderOrFullpath).is_file():
            Error("Missing file %s %s" % (folderOrFullpath, addendumTxt))


def WarnIfNoFile(folderOrFullpath: str, filename=None, addendumTxt="") -> None:
    if filename is not None:
        fullpath = pathlib.Path(folderOrFullpath) / filename
        if not fullpath.is_file():
            Warn("Missing file %s %s" % (fullpath, addendumTxt))
    else:
        if not pathlib.Path(folderOrFullpath).is_file():
            Warn("Missing file %s %s" % (folderOrFullpath, addendumTxt))
