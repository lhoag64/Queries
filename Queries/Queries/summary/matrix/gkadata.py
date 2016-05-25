import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
from   summary.summaryitem          import SummaryItem
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class GkaData(MatrixData):

  _titleDict =                              \
    {                                       \
      'GKA':('Global Key Accounts')   \
    }

#----------------------------------------------------------------------
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
    self.dataDict = Db.QueryGka.GetData(self.regionList,self.weekDict)

    #self.gkaDict  = Db.QueryGkaList.GetData()

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
    #result['DATA'] = [[super()._calcTitleText('Global Key Accounts',self.regionList,self.period)]]
    result['ROWS'] = 1
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _getRowDataHdrDict(self,tblItem):
#    result = super()._initTblItem(tblItem)
#
#    result['DATA'] = []
#    for item in self.gkaDict:
#      text = self.gkaDict[item]
#      result['DATA'].append([text])
#    result['ROWS'] = len(result['DATA'])
#    result['COLS'] = 1
#
#    return result

    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['RHDR']
    result['ROWS'] = self.dataDict['TBL-DATA']['ROWS']
    result['COLS'] = 1

    return result


  #--------------------------------------------------------------------
  def _getColDataHdrDict(self,tblItem):
#    result = super()._initTblItem(tblItem)
#
#    result['DATA'] = [super().calcWeekNumTextList(self.weekDict['MAX'])]
#    result['ROWS'] = 1
#    result['COLS'] = len(result['DATA'][0])
#
#    return result

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
#    rowCompHdrDict = super()._calcRowCompHdrDict()
#    result = super()._initTblItem(tblItem)
#    result['DATA'] = rowCompHdrDict['DATA']
#    result['ROWS'] = rowCompHdrDict['ROWS']
#    result['COLS'] = rowCompHdrDict['COLS']

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
#    colCompHdrDict = super()._calcColCompHdrDict()
#    result = super()._initTblItem(tblItem)
#    result['DATA'] = colCompHdrDict['DATA']
#    result['ROWS'] = colCompHdrDict['ROWS']
#    result['COLS'] = colCompHdrDict['COLS']

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

