import logging
from   database.database            import Database as Db
from   summary.matrix.matrixdata    import MatrixData
from   database.queries.getweeks    import GetWeeks
from   database.queries.getutldtsum import GetUtlDtSum

#----------------------------------------------------------------------
class UtlDtData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__()

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    dataList = GetUtlDtSum(Db.db,regionList,weekDict)

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
    super().calcTitle('Utilisation (Downtime, Exc Leave and Sickness)',regionList,period)
    self.title.fmt['fill'] = 'Red 1'
    
    rowHdrData = ['For','Total Time','Utilisation as a %']
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)
