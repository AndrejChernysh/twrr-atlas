import hashlib
import random
import singletons.Get as Get


def isFactionId(possibleFactionId):
    return possibleFactionId in Get.AllFactionIds()


def delimitedStringToList(separatedString, separator=","):
    if separatedString is None:
        return []
    if separator in separatedString:
        return [i.strip() for i in separatedString.split(separator)]
    else:
        return [separatedString.strip()]


def intWithPossibleRange(integerWithPossibleRange):
    if "-" in str(integerWithPossibleRange) and not str(integerWithPossibleRange[0]) == "-":
        try:
            min = int(integerWithPossibleRange.split("-")[0])
            max = int(integerWithPossibleRange.split("-")[1])
            return random.randint(min, max)
        except TypeError:
            return int(integerWithPossibleRange)
    else:
        return int(integerWithPossibleRange)


def intOrStringWithPossibleRange(integerOrStringWithPossibleRange):
    integerOrStringWithPossibleRange = str(integerOrStringWithPossibleRange)
    if "-" in integerOrStringWithPossibleRange:
        try:
            min = int(integerOrStringWithPossibleRange.split("-")[0])
            max = int(integerOrStringWithPossibleRange.split("-")[1])
            return random.randint(min, max)
        except ValueError:
            if integerOrStringWithPossibleRange.isdigit():
                return int(integerOrStringWithPossibleRange)
            return str(integerOrStringWithPossibleRange)
    else:
        if integerOrStringWithPossibleRange.isdigit():
            return int(integerOrStringWithPossibleRange)
        return str(integerOrStringWithPossibleRange)


def Hash(stringToHash):
    hashObject = hashlib.new("SHA1")
    hashObject.update(stringToHash.encode())
    return str(hashObject.hexdigest()).upper()
