import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
#from   summary.summaryitem          import SummaryItem
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class UtlData(MatrixData):

  _titleDict =                                                                   \
    {                                                                            \
      'UTL-CF':('Utilisation (On Customer Funded Works'            ,'Green 1' ), \
      'UTL-PS':('Utilisation (On Pre-Sales Works'                  ,'Orange 1'), \
      'UTL-DT':('Utilisation (Downtime, Exc Leave and Sickness'    ,'Red 1'   ), \
      'UTL-LS':('Utilisation (Leave and Sickness'                  ,'Yellow 1'), \
      'UTL-OT':('Additional Hours vs Contracted Hours'             ,None      ), \
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
    self.dataDict = Db.QueryUtl.GetData(self.regionList,self.weekDict,qtype=self.objName)

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
    title  = self._titleDict[self.objName][0]
    fmt    = self._titleDict[self.objName][1]
    result = super()._calcTitleDict(title,tblItem)
    if (fmt != None):
      result['FMT' ]['fill'] = fmt

    return result

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


