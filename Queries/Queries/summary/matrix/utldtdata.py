import logging
from   database.database     import Database as Db
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class UtlDtData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    data = Db.TsEntryTbl.GetUtlDtSum(Db.db,region,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,3,weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Utilisation (Downtime, Exc Leave and Sickness)'
    self.titleFmt = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Red 1'}

    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = ['For','Total Time','Utilisation as a %']

    self.rowCompDesc = []