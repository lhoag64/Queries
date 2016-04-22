import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class LtsData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.GetWeeks(period)
    lts      = Db.GetLts('ALL')

    data = Db.GetLtsSum(region,lts,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(lts),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Labour vs Travel'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = []
    for i in range(self.dataRows):
      self.rowDesc.append(lts[i][0])

    self.rowCompDesc = []




