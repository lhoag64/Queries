import logging
from   database.database         import Database as Db
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class FaeLtData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    data     = Db.TsEntryTbl.GetFaeLtSum(Db.db,region,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)

    rowAvgList = super().calcRowAvg(rowSumList,weeks)
    self.compData = [rowAvgList]

    self.data     = super().calcData(data,2,weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Internal vs Contract Hours'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.compCols = len(self.compData)
    self.colCompDesc = ['Avg']

    self.rowDesc = ['Internal Hours','Contractor Hours']

    self.rowCompDesc = []
