import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class ActivityData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.GetWeeks(period)
    act      = Db.GetActivities('ALL')

    data = Db.GetActivitySum(region,act,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(act),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Activity'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = []
    for i in range(self.dataRows):
      self.rowDesc.append(act[i][1] + '-' + str(act[i][0]))

    self.rowCompDesc = []

#    data = [[None for i in range(dataCols)] for j in range(dataRows)]
#    for i in range(dataCols):
#      for j in range(dataRows):
#        data[i][j] = 0.0

#    colSumList = []
#    for i in range(len(data)):
#      sum = 0.0
#      for j in range(len(data[0])):
#        sum += data[i][j]
#      colSumList.append(sum)
#          
#    rowSumList = []
#    for j in range(len(data[0])):
#      sum = 0.0
#      for i in range(len(data)):
#        sum += data[i][j]
#      rowSumList.append(sum)
#          
#    count = 0.0
#    for i in range(len(colSumList)):
#      if (colSumList[i] > 0.0):
#        count += 1.0
#
#    rowAvgList = []
#    for i in range(len(rowSumList)):
#      rowAvgList.append(rowSumList[i] / count)

#    self.data = [[0.0 for j in range(len(act))] for i in range(int(count))]
#    for i in range(int(count)):
#      for j in range(len(act)):
#        self.data[i][j] = data[i][j]

