import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class ActByLocData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period,**kwargs):

    super().__init__()

    weekList = Db.GetWeeks(period)

    actList = Db.GetActivities('ALL')
    act     = kwargs['act']
    locList = kwargs['loc']

    actDesc = ''
    for item in actList:
      if (item[0] == act):
        actDesc = item[1]
        break
    title = actDesc + ' - ' + str(act)

    data = Db.GetActByLocSum(region,act,locList,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(locList),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])


    self.title = title
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = locList

    self.rowCompDesc = []