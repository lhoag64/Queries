import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
from   summary.summaryitem          import SummaryItem
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class UtlData(MatrixData):

  _titleDict =                                                               \
    {                                                                        \
      'UTL-CF':('Utilisation (On Customer Funded Works'        ,'Green 1') , \
      'UTL-PS':('Utilisation (On Pre-Sales Works'              ,'Orange 1'), \
      'UTL-DT':('Utilisation (Downtime, Exc Leave and Sickness','Red 1')   , \
      'UTL-LS':('Utilisation (Leave and Sickness'              ,'Yellow 1'), \
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
    self.dataDict = Db.QueryUtl.GetData(self.regionList,self.weekDict,qtype=self.rptName)

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
  
    title = self._titleDict[self.rptName][0]
    fmt   = self._titleDict[self.rptName][1]
      
    result['DATA'] = [[super()._calcTitleText(title,self.regionList,self.period)]]
    result['ROWS'] = 1
    result['COLS'] = 1
    result['FMT' ]['fill'] = fmt

    return result

  #--------------------------------------------------------------------
  def _getRowDataHdrDict(self,tblItem):
    result = super()._initTblItem(tblItem)

    #utlDict = OrderedDict()
    #utlDict['DATA' ] = 'For'
    #utlDict['TOTAL'] = 'Total Time'

    utlList = ['For','Total Time']

    result['DATA'] = []
    for item in utlList:
      text = item
      result['DATA'].append([text])
    result['ROWS'] = len(result['DATA'])
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _getColDataHdrDict(self,tblItem):
    result = super()._initTblItem(tblItem)

    result['DATA'] = [super().calcWeekNumTextList(self.weekDict['MAX'])]
    result['ROWS'] = 1
    result['COLS'] = len(result['DATA'][0])

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
    rowCompHdrDict = super()._calcRowCompHdrDict()
    result = super()._initTblItem(tblItem)

    result['DATA'] = rowCompHdrDict['DATA']
    result['ROWS'] = rowCompHdrDict['ROWS']
    result['COLS'] = rowCompHdrDict['COLS']

    result['UTL' ] = 'Utilisation as a %'
    result['DATA'].insert(0,[result['UTL']])
    result['ROWS'] += 1

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
    colCompHdrDict = super()._calcColCompHdrDict()
    result = super()._initTblItem(tblItem)
    result['DATA'] = colCompHdrDict['DATA']
    result['ROWS'] = colCompHdrDict['ROWS']
    result['COLS'] = colCompHdrDict['COLS']

    return result

  #--------------------------------------------------------------------
  def _getColCompTblDict(self,tblItem):
    result = super()._initTblItem(tblItem)
    result['DATA'] = self.dataDict['COL-COMP']['DATA']
    result['ROWS'] = self.dataDict['COL-COMP']['ROWS']
    result['COLS'] = self.dataDict['COL-COMP']['COLS']

    return result
