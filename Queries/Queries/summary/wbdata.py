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
from   summary.matrix.nameddata          import NamedData
from   summary.summary.stddata           import StdData
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
    'SUMMARY_STD'      : StdData         \
  }

#----------------------------------------------------------------------
class WbData:

  #--------------------------------------------------------------------
  class Wb:
    def __init__(self):
      self.wbWsDict = OrderedDict()
      self.wb = XlWorkBook()
      ws = self.wb.GetActiveSheet()
      self.wb.SetName(ws,'Summary')
      self.wbWsDict['Summary'] = ws

    #------------------------------------------------------------------
#    def AddSheet(self,wsName,itemDict,fullDict):
#      ws = self.wb.CreateXlWorkSheet(wsName)
#      sheet = WbData.Ws(ws,itemDict,fullDict)
#      self.wsDict[wsName] = (sheet,ws,wsName)
#      return ws
    def AddSheet(self,wsName):
      ws = self.wb.CreateXlWorkSheet(wsName)
      sheet = WbData.Ws(ws)
      self.wbWsDict[wsName] = (ws,sheet,wsName)

    def GetSheet(self,wsName):
      if (wsName in self.wbWsDict):
        return self.wbWsDict[wsName][1]
      else:
        logging.error('WsName not in Workbook: ' + wsName)
        raise

    #------------------------------------------------------------------
    def Order(self):
      self.wb.RemoveSheetByName('Summary')

    #------------------------------------------------------------------
    def Save(self,filename):
      self.wb.Save(filename)

  #--------------------------------------------------------------------
  class Ws:

    #def __init__(self,ws,itemDict,fullDict):
    def __init__(self,ws):
      self.ws       = ws
      self.itemDict = OrderedDict()
      self.objDict  = OrderedDict()

      self.startRow  = 2
      self.startCol = 2

      self.prevRow = self.startRow
      self.prevCol = self.startCol
      self.prevHgt = 0
      self.prevWid = 0


    #--------------------------------------------------------------------
    def calcStartLoc(self,item):
      row = item.loc[0].strip()
      col = item.loc[1].strip()

      rowRelative = False
      if (row[:1] == '+'):
        rowRelative = True
      #row = row[1:]
      colRelative = False
      if (col[:1] == '+'):
        colRelative = True
      #col = col[1:]

      row = int(row)
      col = int(col)
  
      if (row == 0): row = self.startRow
      if (col == 0): col = self.startCol

      if (rowRelative == True):
        row = self.prevRow + self.prevHgt + 2
      if (colRelative == True):
        col = self.prevCol + self.prevWid + 2

      return (row,col)

    #------------------------------------------------------------------
    def AddMatrix(self,item):
      row,col = self.calcStartLoc(item)
      tbl = MatrixTable(self.ws,self,row,col,item)
      item.AddWsObj(self,self.ws,tbl)

      self.prevRow = row
      self.prevCol = col
      self.prevHgt = item.hgt
      self.prevWid = item.wid

    #------------------------------------------------------------------
    def AddSummary(self,item,nameDict):
      row,col = self.calcStartLoc(item)
      tbl = SummaryTable(self.ws,self,row,col,item,nameDict)
      item.AddWsObj(self,self.ws,tbl)

      self.prevRow = row
      self.prevCol = col
      self.prevHgt = item.hgt
      self.prevWid = item.wid

#      for name in itemDict:
#        item = itemDict[name]
#        row,col = self.calcStartLoc(item)
#        if (item.objType == 'MATRIX'):
#          item.AddWsObj(ws,MatrixTable(ws,row,col,item.data))
#        if (item.objType == 'SUMMARY'):
#          item.AddWsObj(ws,SummaryTable(ws,row,col,item.data))
#        self.prevRow = row
#        self.prevCol = col
#        self.prevHgt = item.hgt
#        self.prevWid = item.wid

  #--------------------------------------------------------------------
  # Start of WbData
  #--------------------------------------------------------------------
  def __init__(self):
    self.wb                  = WbData.Wb()
    self.itemDict            = OrderedDict()
    self.itemDict['ALL'    ] = OrderedDict()
    self.itemDict['MATRIX' ] = OrderedDict()
    self.itemDict['SUMMARY'] = OrderedDict()
    self.itemDict['CHART'  ] = OrderedDict()
    self.nameDict            = OrderedDict()
    self.objNameDict         = OrderedDict()
    self.wsDict              = OrderedDict()

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
              if (range not in self.nameDict):
                self.nameDict[range] = rangeData
              else:
                logging.error('Duplicate name in name range dict: ' + range)
              wsName  = NamedData.GetWsName(range)
              objName = NamedData.StripWsName(range)
              if (objName not in self.objNameDict):
                self.objNameDict[objName] = (rangeData,wsName)
              else:
                logging.error('Duplicate name in obj name range dict: ' + range)

  #--------------------------------------------------------------------
  def _updateNameDict(self):
    for name in self.itemDict['MATRIX']:
      item = self.itemDict['MATRIX'][name]
      for name in item.wsObj.names:
        tup = item.wsObj.names[name]
        if (name in self.nameDict):
          rangeData = self.nameDict[name]
          if (rangeData.name != tup[1].name):
            logging.error('Names don\'t match in name database')
            raise
          self.nameDict[name] = tup
          wsName  = NamedData.GetWsName(name)
          objName = NamedData.StripWsName(name)
          tup = (tup[0],tup[1],wsName)
          if (objName in self.objNameDict):
            self.objNameDict[objName] = tup 
          else:
            logging.error('Obj Named Range not in names: ' + name)
        else:
          logging.error('Named Range not in names: ' + name)

#      for section in item.data:
#        if (type(item.data[section]) is OrderedDict):
#          sectionDict = item.data[section]
#          if ('NAMED-RANGES' in sectionDict):
#            for range in item.data[section]['NAMED-RANGES']:
#              rangeData = item.data[section]['NAMED-RANGES'][range]
#              self.nameDict[range] = rangeData

  #--------------------------------------------------------------------
  def _generateSummaryData(self):
    for name in self.itemDict['SUMMARY']:
      item     = self.itemDict['SUMMARY'][name]
      itemDict = self.itemDict['MATRIX']
      nameDict = self.nameDict
      objNameDict = self.objNameDict
      item.CreateSummaryData(FuncDict[item.objFunc],item,itemDict,nameDict,objNameDict)

  #--------------------------------------------------------------------
#  def _generateWsDict(self):
#    for name in self.itemDict['ALL']:
#      item = self.itemDict['ALL'][name]
#      if (item.wsName not in self.wsDict):
#        self.wsDict[item.wsName] = OrderedDict()
#      if (item.fullName not in self.wsDict[item.wsName]):
#        self.wsDict[item.wsName][item.fullName] = item
#      else:
#        logging.error('Duplicate item in worksheet list: ' + item.fullName)
     
  #--------------------------------------------------------------------
  def Process(self):

    self._generateMatixData()
#    self._generateWsDict()
    self._generateSummaryData()

    wsList = []
    wsSet  = set()
    for name in self.itemDict['ALL']:
      item = self.itemDict['ALL'][name]
      if (item.wsName not in wsSet):
        wsSet.add(item.wsName)
        wsList.append(item.wsName)

    for wsName in wsList:
      self.wb.AddSheet(wsName)
      self.wsDict[wsName] = OrderedDict()

    for name in self.itemDict['MATRIX']:
      matrix = self.itemDict['MATRIX'][name]
      wsName = matrix.wsName
      sheet  = self.wb.GetSheet(wsName)
      sheet.AddMatrix(matrix)
      self.wsDict[wsName][matrix.fullName] = matrix

    self._updateNameDict()

    for name in self.itemDict['SUMMARY']:
      summary = self.itemDict['SUMMARY'][name]
      wsName = summary.wsName
      sheet  = self.wb.GetSheet(wsName)
      sheet.AddSummary(summary,self.nameDict)
      self.wsDict[wsName][summary.fullName] = summary

  #--------------------------------------------------------------------
  def Order(self):
    self.wb.Order()

  #--------------------------------------------------------------------
  def Save(self,filename):
    self.wb.Save(filename)

