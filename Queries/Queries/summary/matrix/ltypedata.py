import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
from   summary.summaryitem          import SummaryItem
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class LTypeData(MatrixData):

  _titleDict =                                 \
    {                                          \
      'LTYPE':('Internal vs Contract Hours')   \
    }

  #--------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    funcTbl = OrderedDict()
    funcTbl['TITLE'       ] = self._getTitleDict
    funcTbl['ROW-DATA-HDR'] = self._getRowDataHdrDict
    funcTbl['COL-DATA-HDR'] = self._getColDataHdrDict
    funcTbl['TBL-DATA'    ] = self._getDataTblDict
    funcTbl['ROW-COMP-HDR'] = self._getRowCompHdrDict
    funcTbl['ROW-COMP-TBL'] = self._getRowCompTblDict
    funcTbl['COL-COMP-HDR'] = self._getColCompHdrDict
    funcTbl['COL-COMP-TBL'] = self._getColCompTblDict

    self.regionList = super().calcRegionList(self.region)

    #------------------------------------------------------------------
    # Fetch data from database
    #------------------------------------------------------------------
    self.weekDict = Db.QueryWeeks.GetData(self.regionList,self.period)
    self.dataDict = Db.QueryLType.GetData(self.regionList,self.weekDict)

    for tblItem in self.tbl:
      if (tblItem in funcTbl):
        self.tbl[tblItem] = funcTbl[tblItem](tblItem)

    #------------------------------------------------------------------
    # Calculate overall size
    #------------------------------------------------------------------
    super().calcSize()

    #------------------------------------------------------------------
    # Add named ranges
    #------------------------------------------------------------------
    self.rangeList = []

  #--------------------------------------------------------------------
  def _getTitleDict(self,tblItem):
    result = super()._initTblItem(tblItem)

    title = self._titleDict[self.rptName]

    result['DATA'] = [[super()._calcTitleText(title,self.regionList,self.period)]]
    result['ROWS'] = 1
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _getRowDataHdrDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['RHDR']
    result['ROWS'] = self.dataDict['TBL-DATA']['ROWS']
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _getColDataHdrDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['CHDR']
    result['ROWS'] = 1
    result['COLS'] = self.dataDict['TBL-DATA']['COLS']

    return result

  #--------------------------------------------------------------------
  def _getDataTblDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['DATA']
    result['ROWS'] = self.dataDict['TBL-DATA']['ROWS']
    result['COLS'] = self.dataDict['TBL-DATA']['COLS']

    return result

  #--------------------------------------------------------------------
  def _getRowCompHdrDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['ROW-COMP']['RHDR']
    result['ROWS'] = self.dataDict['ROW-COMP']['ROWS']
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _getRowCompTblDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['ROW-COMP']['DATA']
    result['ROWS'] = self.dataDict['ROW-COMP']['ROWS']
    result['COLS'] = self.dataDict['ROW-COMP']['COLS']

    return result

  #--------------------------------------------------------------------
  def _getColCompHdrDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['COL-COMP']['CHDR']
    result['ROWS'] = 1
    result['COLS'] = self.dataDict['COL-COMP']['COLS']

    return result

  #--------------------------------------------------------------------
  def _getColCompTblDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['COL-COMP']['DATA']
    result['ROWS'] = self.dataDict['COL-COMP']['ROWS']
    result['COLS'] = self.dataDict['COL-COMP']['COLS']

    return result




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
##
#    self.rowHdr.AddData(['Internal Hours','Contract Hours'],cols=1,rows=itemCnt,fmt=fmt)
#
#    super().calcSize()
#
#    self.rangeList = []


