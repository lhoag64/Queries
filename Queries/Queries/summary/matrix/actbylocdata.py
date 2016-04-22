import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class ActByLocData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period,**kwargs):

    super().__init__()

    weekList = Db.GetWeeks(period)

    act     = kwargs['act']
    locList = kwargs['loc']

    data = Db.GetActByLocSum(region,act,locList,weekList)

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