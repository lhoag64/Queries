import logging
from   database.database         import Database as Db
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class LtsData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    lts      = Db.TsLtsTbl.GetLts(Db.db,'ALL')

    data = Db.TsEntryTbl.GetLtsSum(Db.db,region,lts,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
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




