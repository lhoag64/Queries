import logging
from   summary.summaryitem        import SummaryItem
from   database.database          import Database as Db
from   summary.matrix.matrixdata  import MatrixData
from   database.queries.getweeks  import GetWeeks
from   database.queries.getlts    import GetLts
from   database.queries.getltssum import GetLtsSum
#----------------------------------------------------------------------
class LtsData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    regionList = super().calcRegionList(self.region)

    weekDict = GetWeeks(Db.db,regionList,self.period)
    ltsList  = GetLts(Db.db,'')
    dataList = GetLtsSum(Db.db,regionList,weekDict,ltsList)

    weekCnt = len(dataList)
    itemCnt = len(dataList[0])

    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
    for week in range(weekCnt):
      for item in range(itemCnt):
        if (dataList[week] != None):
          hours[week][item] = float(dataList[week][item][1])
        else:
          hours[week][item] = None

    self.data.AddData(hours)

    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)

    self.colCompHdr.AddData(['Avg'])
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcTitle('Labour vs Travel',regionList,self.period)

    rowHdrData = []
    for item in ltsList:
      rowHdrData.append(item[0])
    rowHdrData.append('Other')

    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

    super().calcSize()

    self.rangeList = []
