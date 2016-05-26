#import logging
#from  summary.summaryitem            import SummaryItem
#from   database.database             import Database as Db
#from   database.queries.getfaewhsum  import GetFaeWhSum
##from   database.queries.getweeks     import GetWeeks
#from   summary.matrix.matrixdata     import MatrixData
#
##----------------------------------------------------------------------
#class FaeWhData(MatrixData):
##----------------------------------------------------------------------
#  def __init__(self,item):
#
#    super().__init__(item)
#
#    regionList = super().calcRegionList(self.region)
#
#    weekDict = GetWeeks(Db.db,regionList,self.period)
#    dbResult = GetFaeWhSum(Db.db,regionList,weekDict)
#
#    faeList  = dbResult.faeList
#    dataList = dbResult.hoursList
#
#    faeCnt  = len(faeList)
#    weekCnt = len(dataList)
#
#    super().calcFaeData(faeList,faeCnt,dataList,weekCnt)
#    super().calcFaeColCompData(self.data.data,faeList,faeCnt,regionList)
#    super().calcFaeRowCompData(self.data.data,faeList,faeCnt,dataList,weekCnt,regionList)
#
#    super().calcFaeColCompHdr(regionList,['Avg','Contracted\rHours',{'EMEA':'EUWTD','OTHER':'Max Hours'}])
#    super().calcFaeRowCompHdr(regionList)
#
#    self.title.AddData(super().calcTitleText('Working Hours (inc Leave/Holiday)',regionList,self.period))
#    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
#    super().calcFaeRowHdr(faeList)
#
#    super().calcSize()
#
#    self.rangeList = []
