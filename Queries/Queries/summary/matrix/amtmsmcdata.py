import logging
from   database.database       import Database as Db
from   database.tables.tsentry import TsEntryTable
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class AmTmSmcData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    codes = ['QUA','INT']

    weekList = Db.tsdb.weeksTbl.GetWeeks(Db.db,period)
    data = Db.tsdb.tsEntryTbl.GetAmTmSmcSum(Db.db,region,codes,weekList)

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


    self.title = 'Small Cell and Chipsets'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = ['Qualcomm','Intel']

    self.rowCompDesc = []
