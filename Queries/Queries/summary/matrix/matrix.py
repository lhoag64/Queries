import logging
#from   database.database import Database as Db

#----------------------------------------------------------------------
class Matrix:
  #--------------------------------------------------------------------
  def __init__(self):
    self.descCols = 1
    self.dataCols = 0
    self.compCols = 1

    self.descRows = 1
    self.dataRows = 0
    self.compRows = 0

    self.descColWid = 45
    self.dataColWid =  8
    self.compColWid =  8

    self.descRowHgt = 45
    self.dataRowHgt = 15
    self.compRowHgt = 15

    self.titleFmt       = {'hAlign':'C','vAlign':'C','border':{'A':'thin'}}
    self.descRowFmt     = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
    self.descCompRowFmt = self.descRowFmt
    self.descColFmt     = {'hAlign':'C','vAlign':'C','tAlign':90,'border':{'A':'thin'}}
    self.descCompColFmt = self.descColFmt
    self.dataFmt        = {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0.0'}

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
