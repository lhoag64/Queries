import logging
from   summary.summaryitem      import SummaryItem
from   database.database       import Database as Db
from   database.tables.tsentry import TsEntryTable
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class AmRkaData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    raise

    codes = ['ERC','NOK','ALU','SPR','ATT','TMO','QUA','INT','QOR','TER','SKY','OTHERS','COB','TTT','OTH']

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    data = Db.TsEntryTbl.GetAmRkaSum(Db.db,region,codes,weekList)

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


    self.title = 'AM Regional Key Customers'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = ['Ericsson','Nokia','Alcatel-Lucent','Sprint','AT&T','T-Mobile',
                    'Qualcomm','Intel','Qorvo','Teradyne','Skyworks',
                    'Sum of all other customers', \
                    'Cobham', 'Technical Training - All Types','Customer \'Other\'']

    self.rowCompDesc = []

    super().calcSize()

    self.rangeList = []

