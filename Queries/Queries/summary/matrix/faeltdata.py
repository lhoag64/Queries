import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class FaeLtData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.GetWeeks(period)

#    faeList = Db.tsdb.tsEntryTbl.GetFaeList(Db.db,region,period)
#    faeDict = {}
#    for fae in faeList:
#      if ((fae[0],fae[1]) not in faeDict):
#        faeDict[(fae[0],fae[1])] = [fae[2],fae[3],fae[4]]

    weekList = Db.tsdb.weeksTbl.GetWeeks(Db.db,period)
    data = Db.tsdb.tsEntryTbl.GetFaeLtSum(Db.db,region,weekList)

#    data = [[None for i in range(len(result[0]))] for j in range(len(result))]
#    for i in range(len(result)):
#      for j in range(len(result[0])):
#        data[i][j] = result[i][j][2]

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)

    rowAvgList = super().calcRowAvg(rowSumList,weeks)
    self.compData = [rowAvgList]
#    conHrsList = []
#    for fae in faeList:
#      conHrsList.append(fae[2])
#    self.compData = [rowAvgList,conHrsList]

    self.data     = super().calcData(data,2,weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Internal vs Contract Hours'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.compCols = len(self.compData)
    self.colCompDesc = ['Avg']

    self.rowDesc = ['Internal Hours','Contractor Hours']

    #self.rowDesc = []
    #for fae in faeList:
    #  self.rowDesc.append(fae[0] + ' ' + fae[1])

    self.rowCompDesc = []