import logging
from   collections                       import OrderedDict
from   xlinterface.xlworkbook            import XlWorkBook
from   xlinterface.xlworksheet           import XlWorkSheet
from   summary.matrix.matrixdata         import MatrixData 
from   summary.matrix.matrixtable        import MatrixTable
from   summary.summary.summarytable      import SummaryTable
#from   summary.summaryitem               import SummaryItem
from   openpyxl.chart                    import LineChart
from   openpyxl.chart                    import BarChart
from   openpyxl.chart.reference          import Reference


#----------------------------------------------------------------------
class MetricWorkSheet:
  def __init__(self,ws,itemDict,fullDict):
    self.ws       = ws
    self.itemDict = itemDict
#    self.itemList = itemList
#    self.itemDict = OrderedDict()
#
#    for item in itemList:
#      wsItem   = WsItem(item)
#      self.itemDict[wsItem.fullName] = wsItem

#    for name in self.itemDict:
#      item    = self.itemDict[name]
#      func    = item.funcName
#      region  = item.region
#      iName   = item.itemName
#      period  = item.period
#      options = item.options
#      if (options != None):
#        item.AddData(FuncDict[func](region,iName,period,opt=options))
#      else:
#        item.AddData(FuncDict[func](region,iName,period))

    self.startRow  = 2
    self.startCol = 2

    self.prevRow = self.startRow
    self.prevCol = self.startCol
    self.prevHgt = 0
    self.prevWid = 0

    for name in itemDict:
      item = itemDict[name]
      row,col = self.calcStartLoc(item)
      if (item.rptType == 'MATRIX'):
        item.AddWsRpt(MatrixTable(ws,row,col,item.data))
      if (item.rptType == 'SUMMARY'):
        item.AddWsRpt(SummaryTable(ws,row,col,item,fullDict))
      self.prevRow = row
      self.prevCol = col
      self.prevHgt = item.hgt
      self.prevWid = item.wid

#----------------------------------------------------------------------
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


#    startRow = 2
#    startCol = 2
#
#    self.tables = {}
#
#    for item in matrixList:
#      loc     = item[0]
#      type    = item[2]
#      region  = item[1]
#      period  = item[3]
#      options = item[4]
#      if (mType in self.FuncDict):
#
#        #--------------------------------------------------------------
#        # Find where to put it
#        #--------------------------------------------------------------
#        if (loc == 'START'):
#          startRow  = 2
#          startCol  = 2
#        elif (loc == 'RIGHT'):
#          startRow += 0
#          startCol  = table.rightCol + 2
#        elif (loc == 'DOWN-LEFT'):
#          startRow  = table.bottomRow + 2
#          startCol  = 2
#        elif (loc == 'DOWN'):
#          startRow  = table.bottomRow + 2
#          startCol += 0
#
#        if (options != None):
#          data  = self.FuncDict[mType](region,mType,period,opt=options)
#        else:
#          data  = self.FuncDict[mType](region,mType,period)
#        table = MatrixTable(ws,startRow,startCol,data)
#
#      else:
#        logging.debug('Function table does have: ' + mType)


'''

    startRow += data.dataRows + 2

    startRow += data.dataRows + 2

    if (region == 'EMEA'):
      actList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
      locList = ['UK','Sweden','Finland','France','Germany','Other (EMEA)']
      for act in actList:
        data  = ActByLocData(region,'ACT-BY-LOC',period,act=act,loc=locList)
        table = MatrixTable(ws,startRow,startCol,data)
        self.tables['ACT-' + str(act)] = (data,table)

        startRow += data.dataRows + 2

    elif (region == 'AM'):
      data  = ActivityAmDmrData(region,'ACTIVITY-AM-DMR',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['ACTIVITY-AM-DMR'] = (data,table)

      startRow += data.dataRows + 2

      data  = ActivityAmMiData(region,'ACTIVITY-AM-MI',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['ACTIVITY-AM-MI'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmRkaData(region,'AM-RKA',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-RKA'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmTmCarData(region,'AM-TM-CAR',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-TM-CAR'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmTmSmcData(region,'AM-TM-SMC',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-TM-SMC'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmMiRkaData(region,'AM-MI-RKA',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-MI-RKA'] = (data,table)

      startRow += data.dataRows + 2

      actList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
      prdList = ['DMR','MI']
      for act in actList:
        data  = ActByPrdTeamData(region,'ACT-BY-PRD-TEAM',period,act=act,prd=prdList)
        table = MatrixTable(ws,startRow,startCol,data)
        self.tables['ACT-' + str(act)] = (data,table)

        startRow += data.dataRows + 2

    logging.debug('')
'''

