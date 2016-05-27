import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
from   summary.summaryitem          import SummaryItem
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class ActivityData(MatrixData):

  _titleDict =                                 \
    {                                          \
      'ACTIVITY':('Activity')   \
    }

  #--------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)
    super()._calcFuncTable()
    super().calcRegionList(self.region)

    #------------------------------------------------------------------
    # Fetch data from database
    #------------------------------------------------------------------
    self.weekDict = Db.QueryWeeks.GetData(self.regionList,self.period)
    self.dataDict = Db.QueryAct.GetData(self.regionList,self.weekDict)

    for tblItem in self.tbl:
      if (tblItem in self.funcTbl):
        self.tbl[tblItem] = self.funcTbl[tblItem](tblItem)

    #------------------------------------------------------------------
    # Calculate overall size
    #------------------------------------------------------------------
    super().calcSize()

    #------------------------------------------------------------------
    # Add named ranges
    #------------------------------------------------------------------
    self._createNamedRanges()

  #--------------------------------------------------------------------
  def _createTitleDict(self,tblItem):
    title = self._titleDict[self.rptName]
    return super()._calcTitleDict(title,tblItem)

  #--------------------------------------------------------------------
  def _createRowDataHdrDict(self,tblItem):
    result =  super()._calcRowDataHdrDict(tblItem)

    rows = result['ROWS']
    cols = result['COLS']
    nfmt = result['FMT' ]
    gfmt = nfmt.copy()
    ofmt = nfmt.copy()
    ofmt['fill'] = 'Orange 1'
    gfmt['fill'] = 'Green 1'
    fmt  = [[nfmt for col in range(cols)] for row in range(rows)]
    for rowIdx in range(rows):
      for colIdx in range(cols):
        text = result['DATA'][rowIdx][colIdx]
        if (text != None):
          stxt = text.split()
          if (stxt[-1] in ['10','11','14','15','16','17','18','23']):
            fmt[rowIdx][colIdx] = gfmt
          else:
            fmt[rowIdx][colIdx] = ofmt
        else:
            result['DATA'][rowIdx][colIdx] = 'Other (overhead, leave, etc.)'
            fmt[rowIdx][colIdx]  = nfmt

    result['FMT'] = fmt

    return result

  #--------------------------------------------------------------------
  def _createColDataHdrDict(self,tblItem):
    return super()._calcColDataHdrDict(tblItem)

  #--------------------------------------------------------------------
  def _createDataTblDict(self,tblItem):
    return super()._calcDataTblDict(tblItem)

  #--------------------------------------------------------------------
  def _createRowCompHdrDict(self,tblItem):
    return super()._calcRowCompHdrDict(tblItem)

  #--------------------------------------------------------------------
  def _createRowCompTblDict(self,tblItem):
    return super()._calcRowCompTblDict(tblItem)

  #--------------------------------------------------------------------
  def _createColCompHdrDict(self,tblItem):
    return super()._calcColCompHdrDict(tblItem)

  #--------------------------------------------------------------------
  def _createColCompTblDict(self,tblItem):
    return super()._calcColCompTblDict(tblItem)

  #--------------------------------------------------------------------
  def _createNamedRanges(self):
    super()._calcNamedRanges()


