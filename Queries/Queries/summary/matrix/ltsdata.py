import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class LtsData(MatrixData):

  _titleDict =                                 \
    {                                          \
      'LTS':('Labour vs Travel')   \
    }

  #--------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)
    super()._calcFuncTable()

    #------------------------------------------------------------------
    # Fetch data from database
    #------------------------------------------------------------------
    self.weekDict = Db.QueryWeeks.GetData(self.regionDict,self.period)
    self.dataDict = Db.QueryLts.GetData(self.regionDict,self.weekDict)

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
    return super()._calcRowDataHdrDict(tblItem)

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


