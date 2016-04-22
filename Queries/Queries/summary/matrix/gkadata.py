import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class GkaData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.GetWeeks(period)
#    lts      = Db.GetLts('ALL')

    codes = ['ERC','NOK','ALU','OTHERS','COB','TTT','OTH']

    data = Db.GetGkaSum(region,codes,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(codes),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])


    self.title = 'Customers'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = ['Ericsson','Nokia','Alcatel-Lucent','Sum of all other customers', \
                    'Cobham', 'Technical Training - All Types','Customer \'Other\'']
    #for i in range(self.dataRows):
    #  self.rowDesc.append(self.rowDesc)

    self.rowCompDesc = []