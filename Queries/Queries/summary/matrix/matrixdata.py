import logging
#from   database.database import Database as Db

class MatrixDataTitle:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 1
    self.cols     = 1
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt

  def AddData(self,data,cols=None,rows=None,fmt=None):
    self.data = data
    if (type(data) in [list,dict]):
      self.cols = len(data)
      if (type(data[0]) in [list,dict]):
        self.rows = len(data[0])
      else:
        self.rows = 1
    else:
      self.cols = 1
      self.rows = 1
    if (cols) : self.cols = cols
    if (rows) : self.rows = rows
    if (fmt)  : self.fmt  = fmt

class MatrixDataColHdr:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 0
    self.cols     = 0
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt

  def AddData(self,data,cols=None,rows=None,fmt=None):
    self.data = data
    if (type(data) in [list,dict]):
      self.cols = len(data)
      if (type(data[0]) in [list,dict]):
        self.rows = len(data[0])
      else:
        self.rows = 1
    else:
      self.cols = 1
      self.rows = 1
    if (cols) : self.cols = cols
    if (rows) : self.rows = rows
    if (fmt)  : self.fmt  = fmt

class MatrixDataRowHdr:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 0
    self.cols     = 0
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt

  def AddData(self,data,cols=None,rows=None,fmt=None):
    self.data = data
    if (type(data) in [list,dict]):
      self.rows = len(data)
    else:
      self.rows = 1
    if (cols) : self.cols = cols
    if (rows) : self.rows = rows
    if (fmt)  : self.fmt  = fmt

class MatrixDataData:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 0
    self.cols     = 0
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt
  
  def AddData(self,data,cols=None,rows=None,fmt=None):
    self.data = data
    if (type(data) is list):
      self.cols = len(data)
      if (type(data[0]) is list):
        self.rows = len(data[0])
      else:
        self.rows = 1
    else:
      throw
    if (cols) : self.cols = cols
    if (rows) : self.rows = rows
    if (fmt)  : self.fmt  = fmt

  #--------------------------------------------------------------------
#----------------------------------------------------------------------
class MatrixData:

  def __init__(self):

    titleFmt   = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'wrap':True,'font':{'emph':'B'}}
    rowHdrFmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
    colHdrFmt  = {'hAlign':'C','vAlign':'C','tAlign':90,'border':{'A':'thin'},'wrap':True}
    dataFmt    = {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0.0'}

    topHgt  = 55
    leftWid = 45
    dataHgt = 15
    dataWid =  7

    self.title       = MatrixDataTitle(topHgt,leftWid,titleFmt)
    self.rowHdr      = MatrixDataRowHdr(dataHgt,leftWid,rowHdrFmt)
    self.colHdr      = MatrixDataColHdr(topHgt,dataWid,colHdrFmt)
    self.data        = MatrixDataData(dataHgt,dataWid,dataFmt)
    self.rowCompHdr  = MatrixDataRowHdr(dataHgt,leftWid,rowHdrFmt)
    self.rowCompData = MatrixDataData(dataHgt,dataWid,dataFmt)
    self.colCompHdr  = MatrixDataColHdr(topHgt,dataWid,colHdrFmt)
    self.colCompData = MatrixDataData(dataHgt,dataWid,dataFmt)

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
  def calcWeekNumTextList(self,weekNumList):
    weekList = []
    for week in weekNumList:
      weekList.append('Week ' + week[0])
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
  def calcFaeTitle(self,text,regionList,period):
    self.title.AddData(self.calcTitleText(text,regionList,period))

  #--------------------------------------------------------------------
  def calcFaeColHdr(self):
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

