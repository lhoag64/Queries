import logging
from   collections                  import OrderedDict
from   database.database            import Database as Db
from   summary.summaryitem          import SummaryItem
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class UtlData(MatrixData):


#  rowCompHdrDict['PERCENT'] = 'Utilisation as a %'

  rowHdrDict = OrderedDict()
  rowHdrDict['DATA' ] = 'For'
  rowHdrDict['TOTAL'] = 'Total Time'

  titleDict =                                                                \
    {                                                                        \
      'UTL-CF':('Utilisation (On Customer Funded Works'        ,'Green 1') , \
      'UTL-PS':('Utilisation (On Pre-Sales Works'              ,'Orange 1'), \
      'UTL-DT':('Utilisation (Downtime, Exc Leave and Sickness','Red 1')   , \
      'UTL-LS':('Utilisation (Leave and Sickness'              ,'Yellow 1'), \
    }
 
  #--------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    regionList = super().calcRegionList(self.region)

    #------------------------------------------------------------------
    # Fetch data from database
    #------------------------------------------------------------------
    weekDict = Db.QueryWeeks.GetData(regionList,period)
    dataDict = Db.QueryUtl.GetData(regionList,weekDict,qtype=self.rptName)

    #------------------------------------------------------------------
    # Create Title
    #------------------------------------------------------------------
    titleData = self._getTitleData(regionList,period)
    self.title.AddData(titleData,rows=1,cols=1)
    self.title.fmt['fill'] = self.titleDict[self.rptName][1]

    #------------------------------------------------------------------
    # Create and add Row Header (list of descriptions of each row)
    #------------------------------------------------------------------
    rowDataHdrDict = self._getRowDataHdrDict()

    rows = rowDataHdrDict['ROWS']
    cols = rowDataHdrDict['COLS']
    data = super()._calcData(rowDataHdrDict['DATA'],rows,cols)
    self.rowDataHdr.AddData(data,rows=rows,cols=cols)

    #------------------------------------------------------------------
    # Create and add Col Header (list of descriptions of each row)
    #------------------------------------------------------------------
    colDataHdrDict = self._getColDataHdrDict()

    rows = colHdrDict['ROWS']
    cols = colHdrDict['COLS']
    data = super()._calcData(colDataHdrDict['DATA'],rows,cols)
    self.colDataHdr.AddData(data,rows=rows,cols=cols)

    #------------------------------------------------------------------
    # Add report data (actual data from database)
    #------------------------------------------------------------------
    rows = dataDict['DATA']['ROWS']
    cols = dataDict['DATA']['COLS']
    data = dataDict['DATA']['DATA']
    self.dataTbl.AddData(data,rows=rows,cols=cols)

    #------------------------------------------------------------------
    # Create and add computed row headers (bottow rows of table)
    #------------------------------------------------------------------
    rowCompHdrDict = self._getRowCompHdrDict()

    rows = []
    cols = dataDict['ROW-COMP']['COLS']
    data = super()._calcData(dataDict['ROW-COMP']['DATA'],rows,cols)
    self.rowCompHdr.AddData(data,rows=rowCnt,cols=colCnt)

    #------------------------------------------------------------------
    # Create and add computed row table (bottow rows of table)
    #------------------------------------------------------------------
    rowCompTblDict = self._getRowCompTblDict()

    rows = []
    cols = rowCompTblDict['ROW-COMP']['COLS']
    data = super()._calcData(dataDict['ROW-COMP']['DATA'],rows,cols)
    self.rowCompTbl.AddData(data,rows=rowCnt,cols=colCnt)

    #------------------------------------------------------------------
    # Create and add computed col headers (right cols of table)
    #------------------------------------------------------------------
    colCompHdrDict = self._getColCompHdrDict()

    rows = colCompHdrDict['COL-COMP']['ROWS']
    cols = [0,1]
    data = super()._calcData(dataDict['COL-COMP']['DATA'],rows,cols)
    self.colCompHdr.AddData(data,rows=rows,cols=cols)

    #------------------------------------------------------------------
    # Create and add computed col table (right cols of table)
    #------------------------------------------------------------------
    colCompTblDict = self._getColCompTblDict()

    rows = colCompTblDict['DATA']['ROWS']
    cols = colCompTblDict['DATA']['COLS']
    data = colCompTblDict['DATA']['DATA']
    self.colCompTbl.AddData(data,rows=rows,cols=cols)

    #------------------------------------------------------------------
    # Calculate overall size
    #------------------------------------------------------------------
    super().calcSize()

    #------------------------------------------------------------------
    # Add named ranges
    #------------------------------------------------------------------
    self.rangeList = []

  #--------------------------------------------------------------------
  def _getTitleData(self,regionList,period):
    text    = self.titleDict[self.rptName][0]
    return super().calcTitleText(text,regionList,period)

  #--------------------------------------------------------------------
  def _getRowDataHdrDict(self):
    rowDataHdrDict = self.rowHdrDict.values()
    result = OrderedDict()

  #--------------------------------------------------------------------
  def _getColDataHdrDict(self):
    colHdrDict = super().calcWeekNumTextList(weekDict['MAX'])

  #--------------------------------------------------------------------
  def _getRowCompHdrDict(self):
    rowCompHdrData = self.rowCompHdrDict.values()

  #--------------------------------------------------------------------
  def _getRowCompTblDict(self):
    pass

  #--------------------------------------------------------------------
  def _getColCompHdrDict(self):
    colCompHdrData = self.colCompHdrDict.values()

  #--------------------------------------------------------------------
  def _getColCompTblDict(self):
    pass


