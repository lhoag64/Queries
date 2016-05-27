import logging
from   collections                       import OrderedDict
from   summary.wsitem                    import WsItem
from   summary.matrix.actvitivydata      import ActivityData
from   summary.matrix.ltsdata            import LtsData
from   summary.matrix.ltypedata          import LTypeData
from   summary.matrix.utldata            import UtlData
from   summary.matrix.gkadata            import GkaData
from   summary.matrix.actbylocdata       import ActByLocData
from   summary.matrix.faedata            import FaeData
from   summary.summary.summarydata       import SummaryData

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
    'MATRIX_ACT_BY_LOC': ActByLocData,   \
    'SUMMARY'          : SummaryData     \
  }

#----------------------------------------------------------------------
class WbData:
  def __init__(self,workBook):
    self.wb       = workBook
    self.itemDict = OrderedDict()
    self.itemDict['ALL'    ] = OrderedDict()
    self.itemDict['MATRIX' ] = OrderedDict()
    self.itemDict['SUMMARY'] = OrderedDict()
    self.itemDict['CHART'  ] = OrderedDict()
    self.wsDict   = OrderedDict()

  #--------------------------------------------------------------------
  def AddList(self,infoList):
    for info in infoList:
      item = WsItem(info)

      if (item.rptType == 'MATRIX'):
        if (item.fullName not in self.itemDict['MATRIX']):
          self.itemDict['MATRIX'][item.fullName] = item
        else:
          logging.error('Duplicate matix item in ItemList: ' + item.fullName)

      if (item.rptType == 'SUMMARY'):
        if (item.fullName not in self.itemDict['SUMMARY']):
          self.itemDict['SUMMARY'][item.fullName] = item
        else:
          logging.error('Duplicate summary item in ItemList: ' + item.fullName)

      if (item.rptType == 'CHART'):
        if (item.fullName not in self.itemDict['CHART']):
          self.itemDict['CHART'][item.fullName] = item
        else:
          logging.error('Duplicate chart item in ItemList: ' + item.fullName)

      if (item.fullName not in self.itemDict['ALL']):
        self.itemDict['ALL'][item.fullName] = item
      else:
        logging.error('Duplicate item in ItemList: ' + item.fullName)

  #--------------------------------------------------------------------
  def _generateMatixData(self):
    for name in self.itemDict['MATRIX']:
      item = self.itemDict['MATRIX'][name]
      item.AddData(FuncDict[item.rptFunc](item))

  #--------------------------------------------------------------------
  def _generateWsDict(self):
    for name in self.itemDict['ALL']:
      item = self.itemDict['ALL'][name]
      if (item.wsName not in self.wsDict):
        self.wsDict[item.wsName] = OrderedDict()
      if (item.fullName not in self.wsDict[item.wsName]):
        self.wsDict[item.wsName][item.fullName] = item
      else:
        logging.error('Duplicate item in worksheet list: ' + item.fullName)
     
  #--------------------------------------------------------------------
  def Process(self):

    self._generateMatixData()
    self._generateWsDict()
#    self._generateSummaryData()

    for wsName in self.wsDict:
      logging.debug(wsName)
      self.wb.AddSheet(wsName,self.wsDict[wsName],self.wsDict)
