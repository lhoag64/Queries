import logging
from   database.database         import Database as Db
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class ActByPrdTeamData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period,**kwargs):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    actList  = Db.TsActTbl.GetActivities(Db.db,'ALL')

    act     = kwargs['act']
    prdList = kwargs['prd']

    data = Db.TsEntryTbl.GetActByPrdTeam(Db.db,region,act,prdList,weekList)

    actDesc = ''
    for item in actList:
      if (item[0] == act):
        actDesc = item[1]
        break
    title = actDesc + ' - ' + str(act)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(prdList),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])


    self.title = title
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = prdList

    self.rowCompDesc = []