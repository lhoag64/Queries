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
from   summary.charts.utlpiedata         import UtlPieData
from   summary.charts.utllinedata        import UtlLineData
from   summary.charts.charttable         import ChartTable

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
    'CHART_UTL_PIE'    : UtlPieData,     \
    'CHART_UTL_LINE'   : UtlLineData,    \
    'SUMMARY_STD'      : StdData         \
  }

#----------------------------------------------------------------------
class WbData:

  #--------------------------------------------------------------------
  class Wb:

    #------------------------------------------------------------------
    def __init__(self):
      self.wbWsDict = OrderedDict()
      self.wb = XlWorkBook()
      ws = self.wb.GetActiveSheet()
      self.wb.SetName(ws,'Summary')
      self.wbWsDict['Summary'] = ws

    #------------------------------------------------------------------
    def AddSheet(self,wsName):
      ws = self.wb.CreateXlWorkSheet(wsName)
      sheet = WbData.Ws(ws)
      self.wbWsDict[wsName] = (ws,sheet,wsName)

    #------------------------------------------------------------------
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

    def __init__(self,ws):
      self.ws       = ws
      self.itemDict = OrderedDict()
      self.objDict  = OrderedDict()

      self.sRow = 2
      self.sCol = 2

      self.prevRow = self.sRow
      self.prevCol = self.sCol
      self.prevHgt = 0
      self.prevWid = 0

      self.chSRow = 200
      self.chSCol = 200

      self.prevChRow = self.chSRow
      self.prevChCol = self.chSCol
      self.prevChHgt = 0
      self.prevChWid = 0

    #--------------------------------------------------------------------
    def calcStartLoc(self,item):
      row = item.loc[0].strip()
      col = item.loc[1].strip()

      rowRelative = False
      if (row[:1] == '+'):
        rowRelative = True
      colRelative = False
      if (col[:1] == '+'):
        colRelative = True

      row = int(row)
      col = int(col)
  
      if (row == 0): row = self.sRow
      if (col == 0): col = self.sCol

      if (rowRelative == True):
        row = self.prevRow + self.prevHgt + 2
      if (colRelative == True):
        col = self.prevCol + self.prevWid + 2

      return (row,col)

    #--------------------------------------------------------------------
    def calcStartChLoc(self,item):
  
      row = self.prevChRow + self.prevChHgt + 2
      col = self.prevChCol

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

    #------------------------------------------------------------------
    def AddChart(self,item,nameDict):
      row,col = self.calcStartChLoc(item)
      tbl = ChartTable(self.ws,self,row,col,item,nameDict)
      item.AddWsObj(self,self.ws,tbl)

      self.prevChRow = row
      self.prevChCol = col
      self.prevChHgt = item.hgt
      self.prevChWid = item.wid

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

  #--------------------------------------------------------------------
  def _generateSummaryData(self):
    for name in self.itemDict['SUMMARY']:
      item     = self.itemDict['SUMMARY'][name]
      itemDict = self.itemDict['MATRIX']
      nameDict = self.nameDict
      objNameDict = self.objNameDict
      item.CreateSummaryData(FuncDict[item.objFunc],item,itemDict,nameDict,objNameDict)

  #--------------------------------------------------------------------
  def _generateChartData(self):
    for name in self.itemDict['CHART']:
      item     = self.itemDict['CHART'][name]
      itemDict = self.itemDict['MATRIX']
      nameDict = self.nameDict
      objNameDict = self.objNameDict
      item.CreateChartData(FuncDict[item.objFunc],item,itemDict,nameDict,objNameDict)
     
  #--------------------------------------------------------------------
  def Process(self):

    self._generateMatixData()
    self._generateSummaryData()
    self._generateChartData()

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

    for name in self.itemDict['CHART']:
      chart = self.itemDict['CHART'][name]
      wsName = chart.wsName
      sheet  = self.wb.GetSheet(wsName)
      sheet.AddChart(chart,self.nameDict)
      self.wsDict[wsName][chart.fullName] = chart

  #--------------------------------------------------------------------
  def Order(self):
    self.wb.Order()

  #--------------------------------------------------------------------
  def Save(self,filename):
    self.wb.Save(filename)

