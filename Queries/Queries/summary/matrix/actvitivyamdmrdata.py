import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class ActivityAmDmrData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.GetWeeks(period)
    act      = Db.GetActivities('ALL')

    data = Db.tsdb.tsEntryTbl.GetActivityAmDmrSum(Db.db,region,act,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(act),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Mobile Radio Activity'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    gSet = set([10,11,14,15,16,17,18,23])
    self.rowDesc = []
    self.descRowFmt = []
    gFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    oFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1'}
    for i in range(self.dataRows):
      self.rowDesc.append(act[i][1] + '-' + str(act[i][0]))
      if (act[i][0] in gSet):
        self.descRowFmt.append(gFmt)
      else:
        self.descRowFmt.append(oFmt)

    self.rowCompDesc = []


