import PIL
from PIL import ImageEnhance

from classes.RGB import RGB


def Int(myInt):
    if myInt is None:
        return None
    return int(myInt)


def Str(myStr):
    if myStr is None:
        return None
    return str(myStr).strip()


def List(myList):
    if myList is None:
        return []
    return myList


def RGBFromCommaDelimitedString(color: str) -> RGB:
    return RGB(int(color.split(",")[0]), int(color.split(",")[1]), int(color.split(",")[2]))


def ListFromCommaDelimitedString(myString: str) -> list[str]:
    if myString is None:
        return []
    if "," not in myString:
        return [myString]
    return [s.strip() for s in myString.split(",")]


def ImageToGrey(path):
    img = PIL.Image.open(path)
    imgGray = img.convert('L')
    imgGray.save(path)


def ImageBrighten(path):
    img = PIL.Image.open(path)
    enhancer = ImageEnhance.Brightness(img)
    imgOut = enhancer.enhance(1.9)
    imgOut.save(path)


def ImageDarken(path):
    img = PIL.Image.open(path)
    enhancer = ImageEnhance.Brightness(img)
    imgOut = enhancer.enhance(0.3)
    imgOut.save(path)


def ImageResize(path, width, height):
    try:
        img = PIL.Image.open(path)
        imgResized = img.resize((width, height), PIL.Image.ANTIALIAS)
        imgResized.save(path)
    except FileNotFoundError:
        pass
