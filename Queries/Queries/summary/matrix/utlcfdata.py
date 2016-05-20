#import logging
#from   collections                  import OrderedDict
#from   database.database            import Database as Db
#from   summary.summaryitem          import SummaryItem
#from   summary.matrix.matrixdata    import MatrixData
#
##----------------------------------------------------------------------
#class UtlCfData(MatrixData):
#
#  rowHdrDict     = OrderedDict({'DATA':'For','TOTAL':'Total Time'})
#  colCompHdrDict = OrderedDict({'AVG':'Avg','SUM':'Sum'})
#  rowCompHdrList = OrderedDict({'PERCENT':'Utilisation as a %'})
#  titleDict =                                                                \
#    {                                                                        \
#      'UTL-CF':('Utilisation (On Customer Funded Works'        ,'Green 1') , \
#      'UTL-PS':('Utilisation (On Pre-Sales Works'              ,'Orange 1'), \
#      'UTL-DT':('Utilisation (Downtime, Exc Leave and Sickness','Red 1')   , \
#      'UTL-LV':('Utilisation (Leave and Sickness'              ,'Yellow 1'), \
#    }
# 
#  #--------------------------------------------------------------------
#  def __init__(self,item):
#
#    super().__init__(item)
#
#    regionList = super().calcRegionList(self.region)
#
#    weekDict = Db.QueryWeeks.GetData(regionList,self.period)
#    dataDict = Db.QueryUtl.GetData(regionList,weekDict,qtype=self.rptName)
#
#    dataArray = dataDict['DATA']
#    compArray = dataDict['COMP']
#
#    weekCnt = len(dataArray)
#    itemCnt = len(dataArray[0])
#
#    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
#    for week in range(weekCnt):
#      for item in range(itemCnt):
#        if (dataArray[week] != None):
#          hours[week][item] = float(dataArray[week][item])
#        else:
#          hours[week][item] = None
#
#    super().calcTitle('Utilisation (On Customer Funded Works)',regionList,self.period)
#    self.title.fmt['fill'] = 'Green 1'
#
#    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
#    self.rowHdr.AddData(self.rowHdrDict.values(),cols=1,rows=itemCnt)
#
#    self.colCompHdr.AddData(self.colCompHdrDict.values())
#    self.rowCompHdr.AddData(self.rowCompHdrDict.values())
#
#    self.data.AddData(hours)
#
#    rowSumList = super().calcRowSum(hours)
#    rowAvgList = super().calcRowAvg(rowSumList)
#    colCompDataList = [rowAvgList,rowSumList]
#    self.colCompData.AddData(colCompDataList,cols=len(colCompDataList),rows=itemCnt)
#
#    super().calcSize()
#
#    self.rangeList = []
