import logging
from   database.database     import Database as Db
from   summary.matrix.matrixdata import MatrixData

#----------------------------------------------------------------------
class FaeAwhData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    faeList  = Db.TsEntryTbl.GetFaeList(Db.db,region,period)

    faeDict = {}
    for fae in faeList:
      if ((fae[0],fae[1]) not in faeDict):
        faeDict[(fae[0],fae[1])] = [fae[2],fae[3],fae[4]]

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    result   = Db.TsEntryTbl.GetFaeAwhSum(Db.db,region,weekList)

    data = [[None for i in range(len(result[0]))] for j in range(len(result))]
    for i in range(len(result)):
      for j in range(len(result[0])):
        data[i][j] = result[i][j][2]

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)

    rowAvgList = super().calcRowAvg(rowSumList,weeks)
    conHrsList = []
    maxHrsList = []
    for fae in faeList:
      conHrsList.append(fae[2])
      maxHrsList.append(fae[3])
    self.compData = [rowAvgList,conHrsList,maxHrsList]

    self.data = super().calcData(data,len(faeList),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Actual Working Hours'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.compCols = len(self.compData)
    self.colCompDesc = ['Avg','ConHour','EUWTD']

    self.rowDesc = []
    for fae in faeList:
      self.rowDesc.append(fae[0] + ' ' + fae[1])

    self.rowCompDesc = []
