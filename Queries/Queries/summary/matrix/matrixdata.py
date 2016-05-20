import logging
from   collections         import OrderedDict
from   summary.summaryitem import SummaryItem

#class TableSection:
#  def __init__(self,hgt,wid,fmt):
#    self.rows     = 0
#    self.cols     = 0
#    self.hgt      = hgt
#    self.wid      = wid
#    self.data     = None
#    self.fmt      = fmt
#
#  def AddData(self,dataDict,fmt=None):
#    rows     = dataDict['ROWS']
#    cols     = dataDict['COLS']
#    inpData = dataDict['DATA']
#    if (type(rows) is list):
#      rowRange = rows
#      rowCnt   = len(rowRange)
#    else:
#      rowRange = range(rows)
#      rowCnt   = rows
#    if (type(cols) is list):
#      colRange = cols
#      colCnt   = len(colRange)
#    else:
#      colRange = range(cols)
#      colCnt   = cols
#    data = [[None for colIdx in range(colCnt)] for rowIdx in range(rowCnt)]
#    for rowIdx in rowRange:
#      for colIdx in colRange:
#        data[rowIdx][colIdx] = inpData[rowIdx][colIdx]
#
#    self.data = data
#    self.rows = rowCnt
#    self.cols = colCnt
#    if (fmt)  : self.fmt  = fmt

#----------------------------------------------------------------------
class MatrixData:

  titleFmt   = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'wrap':True,'font':{'emph':'B'}}
  rowHdrFmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
  colHdrFmt  = {'hAlign':'C','vAlign':'C','tAlign':90,'border':{'A':'thin'},'wrap':True}
  dataFmt    = {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0.0'}

  topHgt  = 55
  leftWid = 45
  dataHgt = 15
  dataWid =  8

  _tblItems =          \
    [                  \
      'TITLE'       ,  \
      'ROW-DATA-HDR',  \
      'COL-DATA-HDR',  \
      'TBL-DATA'    ,  \
      'ROW-COMP-HDR',  \
      'ROW-COMP-TBL',  \
      'COL-COMP-HDR',  \
      'COL-COMP-TBL'   \
    ]

  _tblItemDefaults =                                 \
    {                                                \
      'TITLE'       : (topHgt,leftWid,titleFmt)  ,   \
      'ROW-DATA-HDR': (dataHgt,leftWid,rowHdrFmt),   \
      'COL-DATA-HDR': (topHgt,dataWid,colHdrFmt) ,   \
      'TBL-DATA'    : (dataHgt,dataWid,dataFmt)  ,   \
      'ROW-COMP-HDR': (dataHgt,leftWid,rowHdrFmt),   \
      'ROW-COMP-TBL': (dataHgt,dataWid,dataFmt)  ,   \
      'COL-COMP-HDR': (topHgt,dataWid,colHdrFmt) ,   \
      'COL-COMP-TBL': (dataHgt,dataWid,dataFmt)      \
    }

  def __init__(self,item):


    self.item    = item
    self.region  = item.region
    self.rptType = item.rptType  # MATRIX
    self.rptName = item.rptName  # UTL-CF
    self.period  = item.period

    name = ''
    if (type(self.region) is list):
      for rgn in self.region:
        name += self.region + '_'
    else:
      name += self.region + '_'
    name += self.rptName + '_'
    name += self.period

    self.tbl = OrderedDict()
    self.tbl['NAME'] = name
    for item in self._tblItems:
      self.tbl[item] = OrderedDict()

  #--------------------------------------------------------------------
  def _calcRowCompHdrDict(self):

    compList = self.dataDict['ROW-COMP']['HDR']
    rows = len(compList)
    cols = 1
    result = OrderedDict()
    result['AVG' ] = compList[0]
    result['SUM' ] = compList[1]
    result['CNT' ] = compList[2]
    result['ROWS'] = rows
    result['COLS'] = cols
    result['DATA'] = [[None for col in range(cols)] for row in range(rows)]
    for rowIdx in range(result['ROWS']):
      for colIdx in range(result['COLS']):
        result['DATA'][rowIdx][colIdx] = compList[rowIdx]

    return result

  #--------------------------------------------------------------------
  def _calcColCompHdrDict(self):

    compList = self.dataDict['COL-COMP']['HDR']
    rows = 1
    cols = len(compList)
    result = OrderedDict()
    result['AVG' ] = compList[0]
    result['SUM' ] = compList[1]
    result['CNT' ] = compList[2]
    result['ROWS'] = rows
    result['COLS'] = cols
    result['DATA'] = [[None for col in range(cols)] for row in range(rows)]
    for rowIdx in range(result['ROWS']):
      for colIdx in range(result['COLS']):
        result['DATA'][rowIdx][colIdx] = compList[colIdx]

    return result

  #--------------------------------------------------------------------
  def _initTblItem(self,tblItem):
    dataDict = OrderedDict()
    tup = self._tblItemDefaults[tblItem]
    dataDict['HGT'] = tup[0]
    dataDict['WID'] = tup[1]
    dataDict['FMT'] = tup[2]

    return dataDict
    
  #--------------------------------------------------------------------
  def calcSize(self):
    colDataHdrRows = self.tbl['COL-DATA-HDR']['ROWS']
    tblDataRows    = self.tbl['TBL-DATA'    ]['ROWS']
    colCompHdrRows = self.tbl['COL-COMP-HDR']['ROWS']

    rowDataHdrCols = self.tbl['ROW-DATA-HDR']['COLS']
    tblDataCols    = self.tbl['TBL-DATA'    ]['COLS']
    rowCompHdrCols = self.tbl['ROW-COMP-HDR']['COLS']

    self.tbl['ROWS'] = colDataHdrRows + tblDataRows + colCompHdrRows
    self.tbl['COLS'] = rowDataHdrCols + tblDataCols + rowCompHdrCols

  #--------------------------------------------------------------------
  def calcRegionList(self,region):

    if (type(region) is list):
      if ('ALL' in region):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = region
    else:
      if (region == 'ALL'):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = [region]

    return regionList

  #--------------------------------------------------------------------
  def calcColSum(self,data):
    colSumList = []
    for i in range(len(data)):
      colCnt = 0
      sum = 0.0
      for j in range(len(data[0])):
        if (data[i] != None):
          if (type(data[i][j]) is float):
            sum += data[i][j]
            colCnt += 1
      colSumList.append((sum,colCnt))
    return colSumList

  #--------------------------------------------------------------------
  def calcRowSum(self,data):
    rowSumList = []
    for j in range(len(data[0])):
      rowCnt = 0
      sum = 0.0
      for i in range(len(data)):
        if (data[i] != None):
          if (type(data[i][j]) is float):
            sum += data[i][j]
            rowCnt += 1
      rowSumList.append((sum,rowCnt))
    return rowSumList

  #--------------------------------------------------------------------
  def calcCols(self,colSumList):
    count = 0
    for i in range(len(colSumList)):
      if (colSumList[i] > 0):
        count += 1
    return count

  #--------------------------------------------------------------------
  def calcColAvg(self,colSumList):
    colAvgList = []
    for i in range(len(colSumList)):
      sum = colSumList[i][0]
      cnt = colSumList[i][1]
      if (cnt != 0):
        colAvgList.append(sum / float(cnt))
      else:
        colAvgList.append(0.0)
    return colAvgList

  #--------------------------------------------------------------------
  def calcRowAvg(self,rowSumList):
    rowAvgList = []
    for i in range(len(rowSumList)):
      sum = rowSumList[i][0]
      cnt = rowSumList[i][1]
      if (cnt != 0):
        rowAvgList.append(sum / float(cnt))
      else:
        rowAvgList.append(0.0)
    return rowAvgList

  #--------------------------------------------------------------------
  def calcData(self,data,rows,cols):
    table = [[0.0 for j in range(rows)] for i in range(cols)]
    for i in range(cols):
      for j in range(rows):
        table[i][j] = data[i][j]
    return table
  
  #--------------------------------------------------------------------
  def _setTblItem(self,tblItem):
    self.tbl[tblItem] = self.tbl[tblItem]['GET']()
    logging.debug('')

  #--------------------------------------------------------------------
  def _calcData(self,inpData,rows,cols):
    if (type(rows) is list):
      rowRange = rows
      rowCnt   = len(rowRange)
    else:
      rowRange = range(rows)
      rowCnt   = rows
    if (type(cols) is list):
      colRange = cols
      colCnt   = len(colRange)
    else:
      colRange = range(cols)
      colCnt   = cols
    outData = [[None for colIdx in range(colCnt)] for rowIdx in range(rowCnt)]
    for rowIdx in rowRange:
      for colIdx in colRange:
        outData[rowIdx][colIdx] = inpData[rowIdx][colIdx]

    result = OrderedDict()
    result['DATA'] = outData
    result['ROWS'] = rowCnt
    result['COLS'] = colCnt

    return outData

  #--------------------------------------------------------------------
  def calcWeekNumTextList(self,weekNumList):
    weekList = []
    for week in weekNumList:
      weekList.append('Week ' + week[1])
    return weekList
  
  #--------------------------------------------------------------------
  def calcTitleText(self,text,regionList,period):
    if (period == 'ALL'): period = 'YTD'
    title = text
    title += '\r'
    if (len(regionList) == 1):
       title += 'Region: '
    else:
       title += 'Regions: '
    title += ','.join(regionList)
    title += '\r'
    title += 'Period: ' + period

    return title

  #--------------------------------------------------------------------
  def calcTitle(self,text,regionList,period):
    self.title.AddData(self.calcTitleText(text,regionList,period))

  #--------------------------------------------------------------------
  def calcColHdr(self):
    self.colHdr.data = []
    for i in range(self.data.cols):
      self.colHdr.data.append('Week ' + str(i+1))
    self.colHdr.cols = len(self.colHdr.data)

  #--------------------------------------------------------------------
  def calcFaeRowHdr(self,faeList):
    pfmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    cfmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Yellow 1'}
    hdrData = []
    hdrFmt  = []
    for fae in faeList:
      name = fae.fname + ' ' + fae.lname
      hdrData.append(name)
      if (fae.lbrType == 'P'):
        hdrFmt.append(pfmt)
      else:
        hdrFmt.append(cfmt)
    self.rowHdr.AddData(hdrData,fmt=hdrFmt)

  #--------------------------------------------------------------------
  def calcFaeColCompHdr(self,regionList,textList=None):

    hdrText = []
    if (not textList):
      hdrText.append('Avg')
    else:
      for item in textList:
        if (type(item) is dict):
          rgnData = None
          for rgn in item:
            if (rgn in regionList):
              rgnData = item[rgn]
              break
          if (not rgnData):
            rgnData = item['OTHER']
          hdrText.append(rgnData)
        else:
          hdrText.append(item)
    if (len(regionList) > 1):
      hdrText.append('Region')

    self.colCompHdr.AddData(hdrText)

  #--------------------------------------------------------------------
  def calcFaeRowCompHdr(self,regionList,textList=None):

    self.rowCompHdr.data = []
    self.rowCompHdr.data.append('Week Average')
    self.rowCompHdr.data.append('HeadCount')
    if ('AM' in regionList):
      self.rowCompHdr.data.append('AM Working Days')
    if ('EMEA' in regionList):
      self.rowCompHdr.data.append('UK Working Days')
      self.rowCompHdr.data.append('FR Working Days')
      self.rowCompHdr.data.append('DE Working Days')
      self.rowCompHdr.data.append('FI Working Days')
      self.rowCompHdr.data.append('SE Working Days')
    if ('GC' in regionList):
      self.rowCompHdr.data.append('GC Working Days')

    self.rowCompHdr.rows = len(self.rowCompHdr.data)

  #--------------------------------------------------------------------
  def calcFaeData(self,faeList,faeCnt,dataList,weekCnt):
    data = [[None for i in range(faeCnt)] for j in range(weekCnt)]
    for i in range(weekCnt):
      for j in range(faeCnt):
        fname = faeList[j].fname
        lname = faeList[j].lname
        if (dataList[i].hours != None):
          tup   = dataList[i].hours[j]
          if (fname != tup[0] and lname != tup[1]):
            logging.error('Database corrupt matching FAE names')
            return None
          data[i][j] = tup[2]
        else:
          data[i][j] = None

    self.data.data = self.calcData(data,faeCnt,weekCnt)
    self.data.cols = weekCnt
    self.data.rows = faeCnt

  #--------------------------------------------------------------------
  def calcFaeColCompData(self,data,faeList,faeCnt,regionList):
    rowAvgList = self.calcRowAvg(self.calcRowSum(data))
    conHrsList = []
    maxHrsList = []
    faeRgnList = []
    for fae in faeList:
      conHrsList.append(fae.nrmHrs)
      maxHrsList.append(fae.maxHrs)
      if (len(regionList) > 1):
        faeRgnList.append(fae.region)

    if (len(regionList) > 1):
      self.colCompData.data = [rowAvgList,conHrsList,maxHrsList,faeRgnList]
    else:
      self.colCompData.data = [rowAvgList,conHrsList,maxHrsList]
    self.colCompData.cols = len(self.colCompData.data)
    self.colCompData.rows = faeCnt

  #--------------------------------------------------------------------
  def calcFaeRowCompData(self,data,faeList,faeCnt,dataList,weekCnt,regionList):
    colAvgList = self.calcColAvg(self.calcColSum(data))

    compDataFmt = {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0'}
    self.rowCompData.fmt = compDataFmt
    self.rowCompData.data = [[] for i in range(weekCnt)]
    for i in range(weekCnt):
      if (dataList[i].headCount != None and dataList[i].workingDays != None):
        self.rowCompData.data[i].append(colAvgList[i])
        self.rowCompData.data[i].append(dataList[i].headCount)
        if ('AM' in regionList):
          self.rowCompData.data[i].append(dataList[i].workingDays.am_days)
        if ('EMEA' in regionList):
          self.rowCompData.data[i].append(dataList[i].workingDays.uk_days)
          self.rowCompData.data[i].append(dataList[i].workingDays.fr_days)
          self.rowCompData.data[i].append(dataList[i].workingDays.de_days)
          self.rowCompData.data[i].append(dataList[i].workingDays.fi_days)
          self.rowCompData.data[i].append(dataList[i].workingDays.se_days)
        if ('GC' in regionList):
          self.rowCompData.data[i].append(dataList[i].workingDays.gc_days)
      else:
        self.rowCompData.data[i].append(None)
        self.rowCompData.data[i].append(None)
        if ('AM' in regionList):
          self.rowCompData.data[i].append(None)
        if ('EMEA' in regionList):
          self.rowCompData.data[i].append(None)
          self.rowCompData.data[i].append(None)
          self.rowCompData.data[i].append(None)
          self.rowCompData.data[i].append(None)
          self.rowCompData.data[i].append(None)
        if ('GC' in regionList):
          self.rowCompData.data[i].append(None)

    self.rowCompData.rows = len(self.rowCompData.data[0])
    self.rowCompData.cols = weekCnt

