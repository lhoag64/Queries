import logging
from   summary.summaryitem       import SummaryItem
from   database.database         import Database as Db
from   database.tables.tsentry   import TsEntryTable
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class AmMiRkaData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    raise

    codes = ['QOR','TER','SKY']

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    data = Db.TsEntryTbl.GetAmMiRkaSum(Db.db,region,codes,weekList)

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


    self.title = 'Modular Instruments Regional Key Accounts'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = ['Qorvo','Teradyne','Skyworks']

    self.rowCompDesc = []

    super().calcSize()

    self.rangeList = []
