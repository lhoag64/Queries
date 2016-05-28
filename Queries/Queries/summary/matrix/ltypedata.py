import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
#from   summary.summaryitem          import SummaryItem
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
    super()._calcFuncTable()
    super().calcRegionList(self.region)

    #------------------------------------------------------------------
    # Fetch data from database
    #------------------------------------------------------------------
    self.weekDict = Db.QueryWeeks.GetData(self.regionList,self.period)
    self.dataDict = Db.QueryLType.GetData(self.regionList,self.weekDict)

    #self.faeDict = Db.QueryFae.GetFaeData(self.regionList)

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
    title = self._titleDict[self.objName]
    return super()._calcTitleDict(title,tblItem)

  #--------------------------------------------------------------------
  def _createRowDataHdrDict(self,tblItem):
    result = super()._calcRowDataHdrDict(tblItem)

    rows = result['ROWS']
    cols = result['COLS']
    nfmt = result['FMT' ]
    gfmt = nfmt.copy()
    yfmt = nfmt.copy()
    gfmt['fill'] = 'Green 1'
    yfmt['fill'] = 'Yellow 1'
    fmt  = [[nfmt for col in range(cols)] for row in range(rows)]
    for rowIdx in range(rows):
      for colIdx in range(cols):
        text = result['DATA'][rowIdx][colIdx]
        if (text == 'Internal Hours'):
          fmt[rowIdx][colIdx] = gfmt
        elif (text == 'Contracted Hours'):
          fmt[rowIdx][colIdx] = yfmt
        else:
          logging.error('Invalid labor type: ' + tup[2])

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


