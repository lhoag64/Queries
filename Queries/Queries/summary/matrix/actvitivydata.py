import logging
from   database.database         import Database as Db
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class ActivityData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    actList  = Db.TsActTbl.GetActivities(Db.db,'ALL')

    data = Db.TsEntryTbl.GetActivitySum(Db.db,region,actList,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(actList),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Activity'
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
      self.rowDesc.append(actList[i][1] + '-' + str(actList[i][0]))
      if (actList[i][0] in gSet):
        self.descRowFmt.append(gFmt)
      else:
        self.descRowFmt.append(oFmt)

    self.rowCompDesc = []


