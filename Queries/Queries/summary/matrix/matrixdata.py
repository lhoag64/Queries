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

class MatrixDataColHdr:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 1
    self.cols     = 0
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt

  def AddData(self,data,cols=None,rows=None,fmt=None):
    self.data = data
    if (type(data) in [list,dict]):
      self.cols = len(data)
    else:
      self.cols = 1
    if (cols) : self.cols = cols
    if (rows) : self.rows = rows
    if (fmt)  : self.fmt  = fmt

class MatrixDataRowHdr:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 0
    self.cols     = 1
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
    self.rows     = 1
    self.cols     = 0
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt

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
  def calcFaeTitle(self,text,regionList,period):

    if (period == 'ALL'): period = 'YTD'

    self.title.data  = text
    self.title.data += '\r'
    if (len(regionList) == 1):
       self.title.data += 'Region: '
    else:
       self.title.data += 'Regions: '
    self.title.data += ','.join(regionList)
    self.title.data += '\r'
    self.title.data += 'Period: ' + period

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

