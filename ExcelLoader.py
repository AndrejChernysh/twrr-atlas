
import pandas
import numpy

# noinspection PyUnresolvedReferences
from classes.Faction import Faction
# noinspection PyUnresolvedReferences
from classes.Culture import Culture
# noinspection PyUnresolvedReferences
from classes.Religion import Religion
# noinspection PyUnresolvedReferences
from classes.Unit import Unit
# noinspection PyUnresolvedReferences
from classes.Name import Name
# noinspection PyUnresolvedReferences
from classes.BuildingChain import BuildingChain
# noinspection PyUnresolvedReferences
from classes.Building import Building
# noinspection PyUnresolvedReferences
from classes.Resource import Resource
# noinspection PyUnresolvedReferences
from classes.SettlementLevel import SettlementLevel
# noinspection PyUnresolvedReferences
from classes.RebelFaction import RebelFaction
# noinspection PyUnresolvedReferences
from classes.Setting import Setting
# noinspection PyUnresolvedReferences
from classes.Region import Region
# noinspection PyUnresolvedReferences
from classes.Mount import Mount
# noinspection PyUnresolvedReferences
from classes.Landmark import Landmark
# noinspection PyUnresolvedReferences
from classes.MercPool import MercPool


def loadExcelTableToDataframe(excelFileFullPath, excelSheetName):
    dataframe = pandas.read_excel(excelFileFullPath, sheet_name=excelSheetName)
    dataframeNaNReplacedWithNone = dataframe.replace(numpy.NaN, pandas.NA).where(pandas.notnull(dataframe), None)
    return dataframeNaNReplacedWithNone


def getListFromDataframe(dataframe):
    return dataframe.values.tolist()


def getObjectsListFromExcel(excelFileFullPath, objectName):
    dataframe = loadExcelTableToDataframe(excelFileFullPath, "%ss" % objectName)
    datalist = getListFromDataframe(dataframe)
    objectsList = []
    for c, _ in enumerate(datalist):
        objectsList.append(eval("%s(c, *_)" % objectName))
    return objectsList
