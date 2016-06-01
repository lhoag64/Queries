import logging
from   collections              import OrderedDict
from   summary.objdata          import ObjData
from   summary.matrix.nameddata import NamedData

#----------------------------------------------------------------------
class MatrixData(ObjData):

  titleFmt   = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'wrap':True,'font':{'emph':'B'}}
  rowHdrFmt  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
  colHdrFmt  = {'hAlign':'C','vAlign':'C','tAlign':90,'border':{'A':'thin'},'wrap':True}
  dataFmt    =                                                               \
    {                                                                        \
      'F': {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0.0'}, \
      'I': {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'General'}    \
    }

  topHgt  = 55
  leftWid = 45
  dataHgt = 15
  dataWid =  8

  _tblItems =          \
    [                  \
      'TITLE'       ,  \
      'ROW-DATA-HDR',  \
      'COL-DATA-HDR',  \
      'TBL-DATA'    ,  \
      'ROW-COMP-HDR',  \
      'ROW-COMP-TBL',  \
      'COL-COMP-HDR',  \
      'COL-COMP-TBL'   \
    ]

  _tblItemDefaults =                                 \
    {                                                \
      'TITLE'       : (topHgt,leftWid,titleFmt)  ,   \
      'ROW-DATA-HDR': (dataHgt,leftWid,rowHdrFmt),   \
      'COL-DATA-HDR': (topHgt,dataWid,colHdrFmt) ,   \
      'TBL-DATA'    : (dataHgt,dataWid,dataFmt)  ,   \
      'ROW-COMP-HDR': (dataHgt,leftWid,rowHdrFmt),   \
      'ROW-COMP-TBL': (dataHgt,dataWid,dataFmt)  ,   \
      'COL-COMP-HDR': (topHgt,dataWid,colHdrFmt) ,   \
      'COL-COMP-TBL': (dataHgt,dataWid,dataFmt)      \
    }

  def __init__(self,item):

    super().__init__(item)

    self.funcTbl     = None
    self.namedRanges = None

    self.tbl = OrderedDict()
    self.tbl['NAME'] = item.fullName
    for item in self._tblItems:
      self.tbl[item] = OrderedDict()

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
    rowCompHdrRows = self.tbl['ROW-COMP-HDR']['ROWS']

    titleCols      = self.tbl['TITLE'       ]['COLS']
    colDataHdrCols = self.tbl['COL-DATA-HDR']['COLS']
    colCompHdrCols = self.tbl['COL-COMP-HDR']['COLS']

    self.tbl['ROWS'] = titleRows + rowDataHdrRows + rowCompHdrRows
    self.tbl['COLS'] = titleCols + colDataHdrCols + colCompHdrCols

  #--------------------------------------------------------------------
  #--------------------------------------------------------------------
  def _calcFuncTable(self):

    self.funcTbl = OrderedDict()
    self.funcTbl['TITLE'       ] = self._createTitleDict
    self.funcTbl['ROW-DATA-HDR'] = self._createRowDataHdrDict
    self.funcTbl['COL-DATA-HDR'] = self._createColDataHdrDict
    self.funcTbl['TBL-DATA'    ] = self._createDataTblDict
    self.funcTbl['ROW-COMP-HDR'] = self._createRowCompHdrDict
    self.funcTbl['ROW-COMP-TBL'] = self._createRowCompTblDict
    self.funcTbl['COL-COMP-HDR'] = self._createColCompHdrDict
    self.funcTbl['COL-COMP-TBL'] = self._createColCompTblDict

  #--------------------------------------------------------------------
  def _calcTitleDict(self,title,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = [[self._calcTitleText(title,self.regionDict,self.period)]]
    result['ROWS'] = 1
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _calcRowDataHdrDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['RHDR']
    result['ROWS'] = self.dataDict['TBL-DATA']['ROWS']
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _calcColDataHdrDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['CHDR']
    result['ROWS'] = 1
    result['COLS'] = self.dataDict['TBL-DATA']['COLS']

    return result

  #--------------------------------------------------------------------
  def _calcDataTblDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['TBL-DATA']['DATA']
    result['ROWS'] = self.dataDict['TBL-DATA']['ROWS']
    result['COLS'] = self.dataDict['TBL-DATA']['COLS']

    return result

  #--------------------------------------------------------------------
  def _calcRowCompHdrDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['ROW-COMP']['RHDR']
    result['ROWS'] = self.dataDict['ROW-COMP']['ROWS']
    result['COLS'] = 1

    return result

  #--------------------------------------------------------------------
  def _calcRowCompTblDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['ROW-COMP']['DATA']
    result['ROWS'] = self.dataDict['ROW-COMP']['ROWS']
    result['COLS'] = self.dataDict['ROW-COMP']['COLS']

    return result

  #--------------------------------------------------------------------
  def _calcColCompHdrDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['COL-COMP']['CHDR']
    result['ROWS'] = 1
    result['COLS'] = self.dataDict['COL-COMP']['COLS']

    return result

  #--------------------------------------------------------------------
  def _calcColCompTblDict(self,tblItem):
    result = self._initTblItem(tblItem)
    result['DATA'] = self.dataDict['COL-COMP']['DATA']
    result['ROWS'] = self.dataDict['COL-COMP']['ROWS']
    result['COLS'] = self.dataDict['COL-COMP']['COLS']

    return result

  #--------------------------------------------------------------------
  def _calcDataName(self,tblName,baseName,rType,row,col,key):
    #logging.debug('---------------------------------------------')
    #logging.debug('tblName : ' + tblName)
    #logging.debug('baseName: ' + baseName)
    #logging.debug('rType   : ' + rType)
    #logging.debug('key     : ' + key)

    name  = baseName + '.'
    name += self.tbl[key]['DATA'][row][col].upper() + '.'
    name += rType

    #logging.debug('name    : ' + name)
    #logging.debug('---------------------------------------------')

    return name

  #--------------------------------------------------------------------
  def _calcNamedRanges(self):

    tblName = self.item.fullName
    tbl     = self.tbl

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'TITLE'
    rows = tbl[key]['ROWS']
    cols = tbl[key]['COLS']
    srow = 0
    scol = 0
    data = tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.CELL'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'ROW-DATA-HDR'
    rows = tbl[key]['ROWS']
    cols = tbl[key]['COLS']
    srow = 0
    scol = 0
    data = tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'COL-DATA-HDR'
    rows = tbl[key]['ROWS']
    cols = tbl[key]['COLS']
    srow = 0
    scol = 0
    data = tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'TBL-DATA'
    rows = tbl[key]['ROWS']
    cols = tbl[key]['COLS']
    srow = 0
    scol = 0
    data = tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    for rowIdx in range(rows):
      rows = 1
      cols = tbl[key]['COLS']
      srow = rowIdx
      scol = 0
      data = self.tbl[key]['DATA']
      keys = [key,'DATA']

      name = self._calcDataName(tblName,key,'RANGE',rowIdx,0,'ROW-DATA-HDR')
      namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
      names[namedData.name] = namedData

    self.tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'ROW-COMP-HDR'
    rows = self.tbl[key]['ROWS']
    cols = self.tbl[key]['COLS']
    srow = 0
    scol = 0
    data = self.tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    for rowIdx in range(self.tbl[key]['ROWS']):
      rows = 1
      cols = 1
      srow = rowIdx
      scol = 0
      data = self.tbl[key]['DATA']
      keys = [key,'DATA']

      name = self._calcDataName(tblName,key,'CELL',rowIdx,0,key)
      namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
      names[namedData.name] = namedData

    self.tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'ROW-COMP-TBL'
    rows = self.tbl[key]['ROWS']
    cols = self.tbl[key]['COLS']
    srow = 0
    scol = 0
    data = self.tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    for rowIdx in range(self.tbl[key]['ROWS']):
      rows = 1
      cols = self.tbl[key]['COLS']
      srow = rowIdx
      scol = 0
      data = self.tbl[key]['DATA']
      keys = [key,'DATA']

      name = self._calcDataName(tblName,key,'RANGE',rowIdx,0,'ROW-COMP-HDR')
      namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
      names[namedData.name] = namedData

    self.tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'COL-COMP-HDR'
    rows = self.tbl[key]['ROWS']
    cols = self.tbl[key]['COLS']
    srow = 0
    scol = 0
    data = self.tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    for colIdx in range(self.tbl[key]['COLS']):
      rows = 1
      cols = 1
      srow = 0
      scol = colIdx
      data = self.tbl[key]['DATA']
      keys = [key,'DATA']

      name = self._calcDataName(tblName,key,'CELL',0,colIdx,key)
      namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
      names[namedData.name] = namedData

    self.tbl[key]['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()

    key  = 'COL-COMP-TBL'
    rows = self.tbl[key]['ROWS']
    cols = self.tbl[key]['COLS']
    srow = 0
    scol = 0
    data = self.tbl[key]['DATA']
    keys = [key,'DATA']
    name = key + '.RANGE'

    namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
    names[namedData.name] = namedData

    for colIdx in range(self.tbl[key]['COLS']):
      rows = self.tbl[key]['ROWS']
      cols = 1
      srow = 0
      scol = colIdx
      data = self.tbl[key]['DATA']
      keys = [key,'DATA']

      name = self._calcDataName(tblName,key,'RANGE',0,colIdx,'COL-COMP-HDR')
      namedData = NamedData(tblName,name,rows,cols,srow,scol,data,tbl,keys)
      names[namedData.name] = namedData

    self.tbl[key]['NAMED-RANGES'] = names


