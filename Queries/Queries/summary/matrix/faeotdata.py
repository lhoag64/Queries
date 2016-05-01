import logging
from   database.database     import Database as Db
from   summary.matrix.matrix import Matrix

#----------------------------------------------------------------------
class FaeOtData(Matrix):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.GetWeeks(period)

    faeList = Db.tsdb.tsEntryTbl.GetFaeList(Db.db,region,period)
    faeDict = {}
    for fae in faeList:
      if ((fae[0],fae[1]) not in faeDict):
        faeDict[(fae[0],fae[1])] = [fae[2],fae[3],fae[4]]

    weekList = Db.tsdb.weeksTbl.GetWeeks(Db.db,period)
    result = Db.tsdb.tsEntryTbl.GetFaeOtSum(Db.db,region,weekList)

    data = [[None for i in range(len(result[0]))] for j in range(len(result))]
    for i in range(len(result)):
      for j in range(len(result[0])):
        fname = result[i][j][0]
        lname = result[i][j][1]
        wkHrs = result[i][j][2]
        lvHrs = result[i][j][3]
        nmHrs = float(faeDict[(fname,lname)][0])
        data[i][j] = wkHrs - nmHrs + lvHrs
        #text  = '|' + lname.ljust(14) + '|'
        #text += str(wkHrs).rjust(5) + '|' + str(lvHrs).rjust(5) + '|' + str(nmHrs).rjust(5) + '||'
        #text += str(data[i][j]).rjust(5) + '|'
        #logging.debug(text)
      pass

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)

    rowAvgList = super().calcRowAvg(rowSumList,weeks)
    #conHrsList = []
    #maxHrsList = []
    #for fae in faeList:
    #  conHrsList.append(fae[2])
    #  maxHrsList.append(fae[3])
    self.compData = [rowAvgList]

    self.data     = super().calcData(data,len(faeList),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Additional Hours'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.compCols = len(self.compData)
    self.colCompDesc = ['Avg']

    self.rowDesc = []
    for fae in faeList:
      self.rowDesc.append(fae[0] + ' ' + fae[1])

    self.rowCompDesc = []