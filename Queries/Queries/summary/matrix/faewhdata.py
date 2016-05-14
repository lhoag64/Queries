import logging
from   database.database             import Database as Db
from   database.queries.getfaewhsum  import GetFaeWhSum
from   database.queries.getweeks     import GetWeeks
from   summary.matrix.matrixdata     import MatrixData

#----------------------------------------------------------------------
class FaeWhData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__()

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    dbResult = GetFaeWhSum(Db.db,regionList,weekDict)

    faeList  = dbResult.faeList
    dataList = dbResult.hoursList

    faeCnt  = len(faeList)
    weekCnt = len(dataList)

    super().calcFaeData(faeList,faeCnt,dataList,weekCnt)
    super().calcFaeColCompData(self.data.data,faeList,faeCnt,regionList)
    super().calcFaeRowCompData(self.data.data,faeList,faeCnt,dataList,weekCnt,regionList)

    super().calcFaeColCompHdr(regionList,['Avg','Contracted\rHours',{'EMEA':'EUWTD','OTHER':'Max Hours'}])
    super().calcFaeRowCompHdr(regionList)

    #super().calcTitle('Working Hours (inc Leave/Holiday)',regionList,period)
    #super().calcColHdr()
    self.title.AddData(super().calcTitleText('Working Hours (inc Leave/Holiday)',regionList,period))
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcFaeRowHdr(faeList)


#    super().__init__()
#
#    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
#    faeList  = GetFaeList(Db.db,region,period)
#    result   = GetFaeWhSum(Db.db,region,weekList)
#
#    faeDict = {}
#    for fae in faeList:
#      if ((fae[0],fae[1]) not in faeDict):
#        faeDict[(fae[0],fae[1])] = [fae[2],fae[3],fae[4]]
#
#    data = [[None for i in range(len(result[0][0]))] for j in range(len(result))]
#    for i in range(len(result)):
#      tup = result[i][0]
#      for j in range(len(tup)):
#        data[i][j] = tup[j][2]
#
#    colSumList = super().calcColSum(data)
#    rowSumList = super().calcRowSum(data)
#    weeks      = super().calcCols(colSumList)
#    if (weeks != len(weekList)):
#      weeks = len(weekList)
#
#    rowAvgList = super().calcRowAvg(rowSumList,weeks)
#
#    self.data.data = super().calcData(data,len(faeList),weeks)
#    self.data.cols = len(self.data.data)
#    self.data.rows = len(self.data.data[0])
#
#    conHrsList = []
#    maxHrsList = []
#    for fae in faeList:
#      conHrsList.append(fae[2])
#      maxHrsList.append(fae[3])
#    self.colCompData.data = [rowAvgList,conHrsList,maxHrsList]
#    self.colCompData.cols = len(self.colCompData.data)
#    self.colCompHdr.data  = ['Avg','ConHour','EUWTD']
#
#    self.rowCompData.data = [[None for i in range(8)] for j in range(len(result))]
#    for i in range(len(result)):
#      self.rowCompData.data[i][0] = result[i][1]
#      self.rowCompData.data[i][1] = result[i][2]
#      self.rowCompData.data[i][2] = result[i][3]
#      self.rowCompData.data[i][3] = result[i][4]
#      self.rowCompData.data[i][4] = result[i][5]
#      self.rowCompData.data[i][5] = result[i][6]
#      self.rowCompData.data[i][6] = result[i][7]
#      self.rowCompData.data[i][7] = result[i][8]
#
#    self.title.data = 'Working Hours'
#    self.colHdr.data = []
#    for i in range(self.data.cols):
#      self.colHdr.data.append('Week ' + str(i+1))
#
#
#    self.rowHdr = []
#    tup = result[0][0]
#    for i in range(len(tup)):
#      name = tup[i][0] + ' ' + tup[i][1]
#      self.rowHdr.append(name)
#
#    self.compRows = len(self.compRowData)
#    self.rowCompHdr = ['Week','HC','AM Hours','UK Hours','FR Hours','DE Hours','FI Hours','SE Hours','GC Hours']
#
####