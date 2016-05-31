import logging
from   collections     import OrderedDict
from   summary.objdata import ObjData
#----------------------------------------------------------------------
class ChartData(ObjData):

  titleFmt   = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'wrap':True,'font':{'emph':'B'}}
  rowHdrFmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
  colHdrFmt  = {'hAlign':'C','vAlign':'C','tAlign':0,'border':{'A':'thin'},'wrap':True}
  dataFmt    =                                                               \
    {                                                                        \
      'F': {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0.0'}, \
      'I': {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'General'},    \
      'G': {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'General'}    \
    }

  topHgt  = 15
  leftWid = 45
  dataHgt = 15
  dataWid =  8

  _tblItems =          \
    [                  \
      'TITLE'       ,  \
      'ROW-DATA-HDR',  \
      'COL-DATA-HDR',  \
      'TBL-DATA'    ,  \
    ]

  _tblItemDefaults =                                 \
    {                                                \
      'TITLE'       : (topHgt,leftWid,titleFmt)  ,   \
      'ROW-DATA-HDR': (dataHgt,leftWid,rowHdrFmt),   \
      'COL-DATA-HDR': (topHgt,dataWid,colHdrFmt) ,   \
      'TBL-DATA'    : (dataHgt,dataWid,dataFmt)  ,   \
    }

  #--------------------------------------------------------------------
  def __init__(self,item,itemDict,nameDict,objNameDict):

    super().__init__(item)

    self.itemDict    = itemDict
    self.nameDict    = nameDict
    self.objNameDict = objNameDict

    #self.tbl = OrderedDict()
    #self.tbl['NAME'] = item.fullName
    #for item in self._tblItems:
    #  self.tbl[item] = OrderedDict()
  
  #--------------------------------------------------------------------
  def _initTblItem(self,tblItem):
    dataDict = OrderedDict()
    tup = self._tblItemDefaults[tblItem]
    dataDict['HGT'] = tup[0]
    dataDict['WID'] = tup[1]
    fmt             = tup[2]
    dataDict['FMT'] = fmt.copy()

    return dataDict
    
  #--------------------------------------------------------------------
  def calcSize(self):
    titleRows      = self.tbl['TITLE'       ]['ROWS']
    rowDataHdrRows = self.tbl['ROW-DATA-HDR']['ROWS']

    titleCols      = self.tbl['TITLE'       ]['COLS']
    colDataHdrRows = self.tbl['COL-DATA-HDR']['COLS']

    self.tbl['ROWS'] = titleRows + rowDataHdrRows
    self.tbl['COLS'] = titleCols + colDataHdrCols




