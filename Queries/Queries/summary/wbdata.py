import logging
from   collections                       import OrderedDict
from   xlinterface.xlworkbook            import XlWorkBook
from   xlinterface.xlworksheet           import XlWorkSheet
from   summary.wbitem                    import WbItem
from   summary.matrix.actvitivydata      import ActivityData
from   summary.matrix.ltsdata            import LtsData
from   summary.matrix.ltypedata          import LTypeData
from   summary.matrix.utldata            import UtlData
from   summary.matrix.gkadata            import GkaData
from   summary.matrix.actbylocdata       import ActByLocData
from   summary.matrix.faedata            import FaeData
from   summary.matrix.matrixtable        import MatrixTable
from   summary.summary.summarydata       import SummaryData
from   summary.summary.summarytable      import SummaryTable

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
    'SUMMARY_STD'      : SummaryData     \
  }

#----------------------------------------------------------------------
class WbData:

  #--------------------------------------------------------------------
  class Wb:
    def __init__(self):
      self.wsDict = OrderedDict()
      self.wb = XlWorkBook()
      ws = self.wb.GetActiveSheet()
      self.wb.SetName(ws,'Summary')
      self.wsDict['Summary'] = ws

    #------------------------------------------------------------------
    def AddSheet(self,wsName,itemDict,fullDict):
      ws = self.wb.CreateXlWorkSheet(wsName)
      sheet = WbData.Ws(ws,itemDict,fullDict)
      self.wsDict[wsName] = (sheet,ws,wsName)

    #------------------------------------------------------------------
    def Order(self):
      self.wb.RemoveSheetByName('Summary')

    #------------------------------------------------------------------
    def Save(self,filename):
      self.wb.Save(filename)

  #--------------------------------------------------------------------
  class Ws:

    def __init__(self,ws,itemDict,fullDict):
      self.ws       = ws
      self.itemDict = itemDict

      self.startRow  = 2
      self.startCol = 2

      self.prevRow = self.startRow
      self.prevCol = self.startCol
      self.prevHgt = 0
      self.prevWid = 0

      for name in itemDict:
        item = itemDict[name]
        row,col = self.calcStartLoc(item)
        if (item.objType == 'MATRIX'):
          item.AddWsObj(ws,MatrixTable(ws,row,col,item.data))
        if (item.objType == 'SUMMARY'):
          item.AddWsObj(ws,SummaryTable(ws,row,col,item,fullDict))
        self.prevRow = row
        self.prevCol = col
        self.prevHgt = item.hgt
        self.prevWid = item.wid

    #--------------------------------------------------------------------
    def calcStartLoc(self,item):
      row = item.loc[0]
      col = item.loc[1]

      rowRelative = False
      if (row[:1] == '+'):
        rowRelative = True
      row = row[1:]
      colRelative = False
      if (col[:1] == '+'):
        colRelative = True
      col = col[1:]

      row = int(row)
      col = int(col)
  
      if (row == 0): row = self.startRow
      if (col == 0): col = self.startCol

      if (rowRelative == True):
        row = self.prevRow + self.prevHgt + 2
      if (colRelative == True):
        col = self.prevCol + self.prevWid + 2

      return (row,col)

  #--------------------------------------------------------------------
  # Start of WbData
  #--------------------------------------------------------------------
  def __init__(self):
    self.wb       = WbData.Wb()
    self.itemDict = OrderedDict()
    self.itemDict['ALL'    ] = OrderedDict()
    self.itemDict['MATRIX' ] = OrderedDict()
    self.itemDict['SUMMARY'] = OrderedDict()
    self.itemDict['CHART'  ] = OrderedDict()
    self.nameDict = OrderedDict()
    self.wsDict   = OrderedDict()

  #--------------------------------------------------------------------
  def AddList(self,infoList):
    for info in infoList:
      item = WbItem(info)

      if (item.objType == 'MATRIX'):
        if (item.fullName not in self.itemDict['MATRIX']):
          self.itemDict['MATRIX'][item.fullName] = item
        else:
          logging.error('Duplicate matix item in ItemList: ' + item.fullName)

      if (item.objType == 'SUMMARY'):
        if (item.fullName not in self.itemDict['SUMMARY']):
          self.itemDict['SUMMARY'][item.fullName] = item
        else:
          logging.error('Duplicate summary item in ItemList: ' + item.fullName)

      if (item.objType == 'CHART'):
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
      item.CreateMatrixData(FuncDict[item.objFunc],item)
      for section in item.data:
        if (type(item.data[section]) is OrderedDict):
          sectionDict = item.data[section]
          if ('NAMED-RANGES' in sectionDict):
            for range in item.data[section]['NAMED-RANGES']:
              rangeData = item.data[section]['NAMED-RANGES'][range]
              self.nameDict[range] = rangeData

      logging.debug('')
    logging.debug('')

  #--------------------------------------------------------------------
  def _generateSummaryData(self):
    for name in self.itemDict['SUMMARY']:
      item = self.itemDict['SUMMARY'][name]
      item.CreateSummaryData(FuncDict[item.objFunc],self.itemDict['MATRIX'],self.nameDict)

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
    self._generateSummaryData()

    for wsName in self.wsDict:
      logging.debug(wsName)
      self.wb.AddSheet(wsName,self.wsDict[wsName],self.wsDict)

  #--------------------------------------------------------------------
  def Order(self):
    self.wb.Order()

  #--------------------------------------------------------------------
  def Save(self,filename):
    self.wb.Save(filename)

