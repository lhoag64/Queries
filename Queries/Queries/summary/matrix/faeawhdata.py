import logging
from   database.database             import Database as Db
from   database.queries.getfaelist   import GetFaeList
from   database.queries.getfaeawhsum import GetFaeAwhSum
#import summary.matrix.matrixdata
from   summary.matrix.matrixdata     import MatrixData

#----------------------------------------------------------------------
class FaeAwhData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    faeList  = GetFaeList(Db.db,region,period)
    result   = GetFaeAwhSum(Db.db,region,weekList)

    faeDict = {}
    for fae in faeList:
      if ((fae[0],fae[1]) not in faeDict):
        faeDict[(fae[0],fae[1])] = [fae[2],fae[3],fae[4]]

    data = [[None for i in range(len(result[0]))] for j in range(len(result))]
    for i in range(len(result)):
      for j in range(len(result[i])):
        data[i][j] = result[i][j][2]

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)

    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.data.data = super().calcData(data,len(faeList),weeks)
    self.data.cols = len(self.data.data)
    self.data.rows = len(self.data.data[0])

    conHrsList = []
    maxHrsList = []
    for fae in faeList:
      conHrsList.append(fae[2])
      maxHrsList.append(fae[3])
    self.colCompData.data = [rowAvgList,conHrsList,maxHrsList]
    self.colCompData.cols = len(self.colCompData.data)
    self.colCompHdr.data  = ['Avg','ConHour','EUWTD']

    self.rowCompData.data = [[None for i in range(8)] for j in range(len(result))]
    self.rowCompData.rows = len(self.rowCompData.data)
    self.rowCompData.cols = len(self.rowCompData.data)
    for i in range(len(result)):
      self.rowCompData.data[i][0] = result[i][1]
      self.rowCompData.data[i][1] = result[i][2]
      self.rowCompData.data[i][2] = result[i][3]
      self.rowCompData.data[i][3] = result[i][4]
      self.rowCompData.data[i][4] = result[i][5]
      self.rowCompData.data[i][5] = result[i][6]
      self.rowCompData.data[i][6] = result[i][7]
      self.rowCompData.data[i][7] = result[i][8]

    self.rowCompHdr.data = ['Week','HC','AM Hours','UK Hours','FR Hours','DE Hours','FI Hours','SE Hours','GC Hours']

    self.title.data = 'Actual Working Hours'
    self.colHdr.data = []
    for i in range(self.data.cols):
      self.colHdr.data.append('Week ' + str(i+1))

    self.rowHdr.data = []
    for i in range(self.data.rows):
      tup = result[0][i]
      name = tup[0] + ' ' + tup[1]
      self.rowHdr.data.append(name)

    logging.debug('')

