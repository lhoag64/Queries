import logging
from   database.database       import Database as Db
from   database.tables.tsentry import TsEntryTable
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class AmTmCarData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    codes = ['SPR','ATT','TMO']

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    data = Db.TsEntryTbl.GetAmTmCarSum(Db.db,region,codes,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(codes),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])


    self.title = 'US Carriers'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = ['Sprint','AT&T','T-Mobile']

    self.rowCompDesc = []
