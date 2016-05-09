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

class MatrixDataRowHdr:
  def __init__(self,hgt,wid,fmt):
    self.rows     = 0
    self.cols     = 1
    self.hgt      = hgt
    self.wid      = wid
    self.data     = None
    self.fmt      = fmt

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
  #title       = None
  #rowHdr      = None
  #colHdr      = None
  #data        = None
  #rowCompHdr  = None
  #rowCompData = None
  #colCompHdr  = None
  #colCompData = None

  def __init__(self):

    titleFmt   = {'hAlign':'C','vAlign':'C','border':{'A':'thin'}}
    rowHdrFmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
    colHdrFmt  = {'hAlign':'C','vAlign':'C','tAlign':90,'border':{'A':'thin'}}
    dataFmt    = {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0.0'}

    topHgt  = 20
    leftWid = 45
    dataHgt = 10
    dataWid = 20

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
      sum = 0.0
      for j in range(len(data[0])):
        sum += data[i][j]
      colSumList.append(sum)
    return colSumList

  #--------------------------------------------------------------------
  def calcRowSum(self,data):
    rowSumList = []
    for j in range(len(data[0])):
      sum = 0.0
      for i in range(len(data)):
        sum += data[i][j]
      rowSumList.append(sum)
    return rowSumList

  #--------------------------------------------------------------------
  def calcCols(self,colSumList):
    count = 0
    for i in range(len(colSumList)):
      if (colSumList[i] > 0):
        count += 1
    return count

  #--------------------------------------------------------------------
  def calcRowAvg(self,rowSumList,count):
    rowAvgList = []
    for i in range(len(rowSumList)):
      rowAvgList.append(rowSumList[i] / float(count))
    return rowAvgList

  #--------------------------------------------------------------------
  def calcData(self,data,rows,cols):
    table = [[0.0 for j in range(rows)] for i in range(cols)]
    for i in range(cols):
      for j in range(rows):
        table[i][j] = data[i][j]
    return table
