import logging
from   summary.summaryitem             import SummaryItem
from   database.database               import Database as Db
from   summary.matrix.matrixdata       import MatrixData
#from   database.queries.getweeks       import GetWeeks
from   database.queries.getovertimesum import GetOverTimeSum
#----------------------------------------------------------------------
class OverTimeData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    regionList = super().calcRegionList(self.region)

    weekDict = GetWeeks(Db.db,regionList,self.period)
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
    super().calcTitle('Additional Hours Vs. Contracted Hours',regionList,self.period)

    # TODO: Add HC and hours and other calculated results
    # TODO: Utilisation is really a calculated result
    
    rowHdrData = ['Additional','Contracted','Additional hours as a %']
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

    super().calcSize()

    baseName = self.item.fullName

    data        = self.data
    rowHdr      = self.rowHdr
    colHdr      = self.colHdr
    rowCompHdr  = self.rowCompHdr
    rowCompData = self.rowCompData
    colCompHdr  = self.colCompHdr
    colCompData = self.colCompData

    for i,j in enumerate(data.data):
      name  = baseName + '.'
      #name += 
