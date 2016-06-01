import logging
from   collections                  import OrderedDict
from   summary.charts.chartdata     import ChartData

#----------------------------------------------------------------------
class UtlLineData(ChartData):

  #--------------------------------------------------------------------
  def __init__(self,item,itemDict,nameDict,objNameDict):

    super().__init__(item,itemDict,nameDict,objNameDict)

    regionDict = self.regionDict
    period     = self.period
    # TODO: Fix Hack
    region     = self.regionDict['LIST'][0]
    prefix     = 'MATRIX.' + region + '.' + period + '.'

    #------------------------------------------------------------------
    name   = prefix + 'UTL_CF.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    cfData = objNameDict[name][0]
    name   = prefix + 'UTL_PS.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    psData = objNameDict[name][0]
    name   = prefix + 'UTL_DT.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    dtData = objNameDict[name][0]
    name   = prefix + 'UTL_LS.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    lsData = objNameDict[name][0]

    sRow = cfData.sRow
    sCol = cfData.sCol
    cnt  =   0
    sum  = 0.0
    for rowIdx in range(cfData.rows):
      for colIdx in range(cfData.cols):
        val = cfData.data[sRow + rowIdx][sCol + colIdx]
        if (val != None):
          sum += val
          cnt += 1
    cfAvg = sum/float(cnt)

    sRow = psData.sRow
    sCol = psData.sCol
    cnt  =   0
    sum  = 0.0
    for rowIdx in range(psData.rows):
      for colIdx in range(psData.cols):
        val = psData.data[sRow + rowIdx][sCol + colIdx]
        if (val != None):
          sum += val
          cnt += 1
    psAvg = sum/float(cnt)

    sRow = dtData.sRow
    sCol = dtData.sCol
    cnt  =   0
    sum  = 0.0
    for rowIdx in range(dtData.rows):
      for colIdx in range(dtData.cols):
        val = dtData.data[sRow + rowIdx][sCol + colIdx]
        if (val != None):
          sum += val
          cnt += 1
    dtAvg = sum/float(cnt)

    sRow = lsData.sRow
    sCol = lsData.sCol
    cnt  =   0
    sum  = 0.0
    for rowIdx in range(lsData.rows):
      for colIdx in range(lsData.cols):
        val = lsData.data[sRow + rowIdx][sCol + colIdx]
        if (val != None):
          sum += val
          cnt += 1
    lsAvg = sum/float(cnt)

    #------------------------------------------------------------------
    dataDict = OrderedDict()

    dataDict['NAME'] = item.fullName

    dataDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 1
    data = [['Utilisation' for col in range(cols)] for row in range(rows)]
    dataDict['TITLE']['DATA'] = data
    dataDict['TITLE']['ROWS'] = rows
    dataDict['TITLE']['COLS'] = cols
    tup = self._tblItemDefaults['TITLE']
    dataDict['TITLE']['HGT' ] = tup[0]
    dataDict['TITLE']['WID' ] = tup[1]
    dataDict['TITLE']['FMT' ] = tup[2].copy()

    self._initTblItem('ROW-DATA-HDR')
    dataDict['ROW-DATA-HDR'] = OrderedDict()
    rows = 4
    cols = 1
    data = [['X' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Customer Funded Work'
    data[1][0] = 'Pre-Sales Work'
    data[2][0] = 'Downtime (Exc Leave and Sickness)'
    data[3][0] = 'Leave and Sickness'
    dataDict['ROW-DATA-HDR']['DATA'] = data
    dataDict['ROW-DATA-HDR']['ROWS'] = rows
    dataDict['ROW-DATA-HDR']['COLS'] = cols
    tup = self._tblItemDefaults['ROW-DATA-HDR']
    dataDict['ROW-DATA-HDR']['HGT' ] = tup[0]
    dataDict['ROW-DATA-HDR']['WID' ] = tup[1]
    dataDict['ROW-DATA-HDR']['FMT' ] = tup[2].copy()

    self._initTblItem('COL-DATA-HDR')
    dataDict['COL-DATA-HDR'] = OrderedDict()
    rows = 1
    cols = 1
    data = [['Y' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Pct'
    dataDict['COL-DATA-HDR']['DATA'] = data
    dataDict['COL-DATA-HDR']['ROWS'] = rows
    dataDict['COL-DATA-HDR']['COLS'] = cols
    tup = self._tblItemDefaults['COL-DATA-HDR']
    dataDict['COL-DATA-HDR']['HGT' ] = tup[0]
    dataDict['COL-DATA-HDR']['WID' ] = tup[1]
    dataDict['COL-DATA-HDR']['FMT' ] = tup[2].copy()

    self._initTblItem('TBL-DATA')
    dataDict['TBL-DATA'] = OrderedDict()
    rows = 4
    cols = 1
    data = [['Z' for col in range(cols)] for row in range(rows)]
    data[0][0] = cfAvg
    data[1][0] = psAvg
    data[2][0] = dtAvg
    data[3][0] = lsAvg
    dataDict['TBL-DATA']['DATA'] = data
    dataDict['TBL-DATA']['ROWS'] = rows
    dataDict['TBL-DATA']['COLS'] = cols
    tup = self._tblItemDefaults['TBL-DATA']
    dataDict['TBL-DATA']['HGT' ] = tup[0]
    dataDict['TBL-DATA']['WID' ] = tup[1]
    dataDict['TBL-DATA']['FMT' ] = tup[2].copy()

    dataDict['ROWS'] = 5
    dataDict['COLS'] = 2

    self.tbl = dataDict



