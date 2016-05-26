#import logging
#from   summary.summaryitem          import SummaryItem
#from   database.database            import Database as Db
##from   database.queries.getweeks    import GetWeeks
##from   database.queries.getfaeltsum import GetFaeLtSum
#from   summary.matrix.matrixdata    import MatrixData
#
##----------------------------------------------------------------------
#class FaeLtData(MatrixData):
##----------------------------------------------------------------------
#  def __init__(self,item):
#
#    super().__init__(item)
#
#    regionList = super().calcRegionList(self.region)
#
#    weekDict    = GetWeeks(Db.db,regionList,self.period)
#    dataList    = GetFaeLtSum(Db.db,regionList,weekDict)
#
#    weekCnt = len(dataList)
#    itemCnt = len(dataList[0])
#
#    self.data.AddData(dataList)
#
#    rowAvgList = super().calcRowAvg(super().calcRowSum(dataList))
#    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)
#
#    self.colCompHdr.AddData(['Avg'])
#    self.title.AddData(super().calcTitleText('Internal vs Contract Hours',regionList,self.period))
#    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
#
#    fmt =                                                                    \
#      [                                                                      \
#        {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'},  \
#        {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Yellow 1'}  \
#      ]
#
#    self.rowHdr.AddData(['Internal Hours','Contract Hours'],cols=1,rows=itemCnt,fmt=fmt)
#
#    super().calcSize()
#
#    self.rangeList = []


