import logging
from   database.database               import Database as Db
from   summary.matrix.matrixdata       import MatrixData
from   database.queries.getweeks       import GetWeeks
from   database.queries.getovertimesum import GetOverTimeSum
#----------------------------------------------------------------------
class OverTimeData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__()

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    dataList = GetOverTimeSum(Db.db,regionList,weekDict)

    weekCnt = len(dataList)
    itemCnt = len(dataList[0])

    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
    for week in range(weekCnt):
      for item in range(itemCnt):
        if (dataList[week] != None):
          hours[week][item] = float(dataList[week][item])
        else:
          hours[week][item] = None

    self.data.AddData(hours)

    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)

    self.colCompHdr.AddData(['Avg'])
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcTitle('Additional Hours Vs. Contracted Hours',regionList,period)

    # TODO: Add HC and hours and other calculated results
    # TODO: Utilisation is really a calculated result
    
    rowHdrData = ['Additional','Contracted','Additional hours as a %']
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

#    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
#    data     = Db.TsEntryTbl.GetOverTimeSum(Db.db,region,weekList)
#
#    colSumList = super().calcColSum(data)
#    rowSumList = super().calcRowSum(data)
#    weeks      = super().calcCols(colSumList)
#    if (weeks != len(weekList)):
#      weeks = len(weekList)
#    rowAvgList = super().calcRowAvg(rowSumList,weeks)
#
#    self.compData = [rowAvgList]
#    self.data     = super().calcData(data,3,weeks)
#
#    self.dataCols = len(self.data)
#    self.dataRows = len(self.data[0])
#
#    self.title = 'Additional Hours Vs. Contracted Hours'
#    self.colDesc = []
#    for i in range(self.dataCols):
#      self.colDesc.append('Week ' + str(i+1))
#
#    self.colCompDesc = ['Avg']
#
#    self.rowDesc = ['For','Total Time','Utilisation as a %']
#
#    self.rowCompDesc = []