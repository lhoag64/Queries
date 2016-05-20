import logging
from   summary.summaryitem             import SummaryItem
from   database.database               import Database as Db
from   summary.matrix.matrixdata       import MatrixData
from   database.queries.getweeks       import GetWeeks
from   database.queries.getactbylocsum import GetActByLocSum

#----------------------------------------------------------------------
class ActByLocData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    act = None
    opt = self.item.options
    if (opt):
      if ('ACT' in opt):
        act = opt['ACT']
    if (act == None):
      logging.error('Activity by Location requres activity argument, skipping')
      return


    self.name += '_' + str(act).zfill(2)

    regionList = super().calcRegionList(self.region)

    weekDict = GetWeeks(Db.db,regionList,self.period)
    dataDict = GetActByLocSum(Db.db,regionList,weekDict,act)

    dataList = dataDict['HRSLIST']

    weekCnt = len(dataList)
    itemCnt = len(dataList[0])

    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
    for week in range(weekCnt):
      for item in range(itemCnt):
        if (dataList[week] != None):
          hours[week][item] = float(dataList[week][item][2])
        else:
          hours[week][item] = None

    self.data.AddData(hours)

    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)

    self.colCompHdr.AddData(['Avg'])
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcTitle(dataDict['TITLE'],regionList,self.period)

    rowHdrData = []
    for item in dataDict['GRPLIST']:
      rowHdrData.append(item[1])
    
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

    super().calcSize()

    self.rangeList = []
