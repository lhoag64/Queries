#import logging
#from   database.database            import Database as Db
#from   summary.summaryitem          import SummaryItem
#from   summary.matrix.matrixdata    import MatrixData
#
##----------------------------------------------------------------------
#class UtlPsData(MatrixData):
##----------------------------------------------------------------------
#  def __init__(self,item):
#
#    super().__init__(item)
#
#    regionList = super().calcRegionList(self.region)
#
#    weekDict = db.QueryWeeks.GetData(regionList,self.period)
#    dataList = db.QueryUtl(Db.db,regionList,weekDict,{'QTYPE':''})
#
#    weekCnt = len(dataList)
#    itemCnt = len(dataList[0])
#
#    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
#    for week in range(weekCnt):
#      for item in range(itemCnt):
#        if (dataList[week] != None):
#          hours[week][item] = float(dataList[week][item])
#        else:
#          hours[week][item] = None
#
#    self.data.AddData(hours)
#
#    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
#    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)
#
#    self.colCompHdr.AddData(['Avg'])
#    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
#    super().calcTitle('Utilisation (On Pre-Sales Works)',regionList,self.period)
#    self.title.fmt['fill'] = 'Orange 1'
#    
#    rowHdrData = ['For','Total Time','Utilisation as a %']
#    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)
#
#    super().calcSize()
#
#    self.rangeList = []