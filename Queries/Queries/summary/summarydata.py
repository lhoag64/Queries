import logging
from   collections                       import OrderedDict
from   summary.summaryitem               import SummaryItem
from   summary.matrix.actvitivydata      import ActivityData
#from   summary.matrix.actvitivyamdmrdata import ActivityAmDmrData
#from   summary.matrix.actvitivyammidata  import ActivityAmMiData
from   summary.matrix.ltsdata            import LtsData
from   summary.matrix.ltypedata          import LTypeData
from   summary.matrix.utldata            import UtlData
from   summary.matrix.gkadata            import GkaData
#from   summary.matrix.amrkadata          import AmRkaData
#from   summary.matrix.amtmcardata        import AmTmCarData
#from   summary.matrix.amtmsmcdata        import AmTmSmcData
#from   summary.matrix.ammirkadata        import AmMiRkaData
from   summary.matrix.actbylocdata       import ActByLocData
#from   summary.matrix.actbyprdteamdata   import ActByPrdTeamData
from   summary.matrix.faedata            import FaeData
#from   summary.matrix.faeawhdata         import FaeAwhData
#from   summary.matrix.faewhdata          import FaeWhData
#from   summary.matrix.faeotdata          import FaeOtData

#----------------------------------------------------------------------
FuncDict =                               \
  {                                      \
    'MATRIX_FAE_AWH'   : FaeData,        \
    'MATRIX_FAE_WH'    : FaeData,        \
    'MATRIX_FAE_OT'    : FaeData,        \
    'MATRIX_ACTIVITY'  : ActivityData,   \
    'MATRIX_GKA'       : GkaData,        \
    'MATRIX_LTYPE'     : LTypeData,      \
    'MATRIX_LTS'       : LtsData,        \
    'MATRIX_UTL_CF'    : UtlData,        \
    'MATRIX_UTL_DT'    : UtlData,        \
    'MATRIX_UTL_PS'    : UtlData,        \
    'MATRIX_UTL_LS'    : UtlData,        \
    'MATRIX_UTL_OT'    : UtlData,        \
    'MATRIX_ACT_BY_LOC': ActByLocData    \
  }

#----------------------------------------------------------------------
class SummaryData:
  def __init__(self,workBook):
    self.wb       = workBook
    self.itemDict = OrderedDict()
    self.wsDict   = OrderedDict()

  #--------------------------------------------------------------------
  def AddList(self,infoList):
    for info in infoList:
      item = SummaryItem(info)
      if (item.fullName not in self.itemDict):
        self.itemDict[item.fullName] = item
      else:
        logging.error('Duplicate item in ItemList: ' + item.fullName)

  #--------------------------------------------------------------------
  def _generateData(self):
    for name in self.itemDict:
      item = self.itemDict[name]
      if (item.rptType == 'MATRIX'):
        item.AddData(FuncDict[item.rptFunc](item))

  #--------------------------------------------------------------------
  def _generateWsDict(self):
    for name in self.itemDict:
      item = self.itemDict[name]
      if (item.wsName not in self.wsDict):
        self.wsDict[item.wsName] = OrderedDict()
      if (item.fullName not in self.wsDict[item.wsName]):
        self.wsDict[item.wsName][item.fullName] = item
      else:
        logging.error('Duplicate worksheet ItemList: ' + item.fullName)
     
  #--------------------------------------------------------------------
  def Process(self):

    self._generateData()
    self._generateWsDict()

    for wsName in self.wsDict:
      logging.debug(wsName)
      self.wb.AddSheet(wsName,self.wsDict[wsName],self.wsDict)

    logging.debug('')