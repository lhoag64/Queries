import logging
from   collections         import OrderedDict
#from   summary.summaryitem import SummaryItem

#----------------------------------------------------------------------
class MatrixData:

  class Range:
    def __init__(self,rows,cols,sRow,sCol,data):
      self.rows = rows
      self.cols = cols
      self.sRow = sRow
      self.sCol = sCol
      self.data = data

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

    self.item        = item
    self.region      = item.region
    self.rptType     = item.rptType  # MATRIX
    self.rptName     = item.rptName  # UTL-CF
    self.period      = item.period
    self.funcTbl     = None
    self.regionList  = None
    self.namedRanges = None

    #name = ''
    #if (type(self.region) is list):
    #  for rgn in self.region:
    #    name += self.region + '_'
    #else:
    #  name += self.region + '_'
    #name += self.rptName + '_'
    #name += self.period

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
  def calcRegionList(self,region):

    if (type(region) is list):
      if ('ALL' in region):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = region
    else:
      if (region == 'ALL'):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = [region]

    self.regionList = regionList

    return regionList

  #--------------------------------------------------------------------
  def _calcTitleText(self,text,regionList,period):
    if (period == 'ALL'): period = 'YTD'
    title = text
    title += '\r'
    if (len(regionList) == 1):
       title += 'Region: '
    else:
       title += 'Regions: '
    title += ','.join(regionList)
    title += '\r'
    title += 'Period: ' + period

    return title

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
    result['DATA'] = [[self._calcTitleText(title,self.regionList,self.period)]]
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
  def _calcRangeName(self,fname,baseName,rowIdx,colIdx,tblKey):
    #logging.debug('---------------------------------------------')
    #logging.debug(fname)
    #logging.debug(baseName)
    #logging.debug(str(rowIdx))
    #logging.debug(tblKey)

    tbl = self.tbl[tblKey]

    name = '.'
    for ch in baseName:
      if (ch in ['-',' ']):
        ch = '_'
      name += ch

    name += '.'

    text = tbl['DATA'][rowIdx][colIdx].upper()
    #logging.debug(text)
    for ch in text:
      if (ch == '%'):
        ch = 'PCT'
      elif (ch in ['-',' ']):
        ch = '_'
      name += ch

    #logging.debug('---------------------------------------------')
    #logging.debug(fname + name)
    #logging.debug('---------------------------------------------')

    return fname + name

  #--------------------------------------------------------------------
  def _calcNamedRanges(self):


    fname = self.item.fullName

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.TITLE'
    rows = self.tbl['TITLE']['ROWS']
    cols = self.tbl['TITLE']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['TITLE']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)
    self.tbl['TITLE']['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.ROW_DATA_HDR'
    rows = self.tbl['ROW-DATA-HDR']['ROWS']
    cols = self.tbl['ROW-DATA-HDR']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['ROW-DATA-HDR']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)
    self.tbl['ROW-DATA-HDR']['NAMED-RANGES'] = names
 
    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.COL_DATA_HDR'
    rows = self.tbl['COL-DATA-HDR']['ROWS']
    cols = self.tbl['COL-DATA-HDR']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['COL-DATA-HDR']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)
    self.tbl['COL-DATA-HDR']['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.TBL_DATA'
    rows = self.tbl['TBL-DATA']['ROWS']
    cols = self.tbl['TBL-DATA']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['TBL-DATA']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)
    self.tbl['TBL-DATA']['NAMED-RANGES'] = names

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.ROW_COMP_HDR'
    rows = self.tbl['ROW-COMP-HDR']['ROWS']
    cols = self.tbl['ROW-COMP-HDR']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['ROW-COMP-HDR']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    for rowIdx in range(self.tbl['ROW-COMP-HDR']['ROWS']):
      name = self._calcRangeName(fname,'ROW-COMP-HDR',rowIdx,0,'ROW-COMP-HDR')
      rows = 1
      cols = 1
      srow = rowIdx
      scol = 0
      data = self.tbl['ROW-COMP-HDR']['DATA']
      names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    self.tbl['ROW-COMP-HDR']['NAMED-RANGES'] = names

#    name = fname + '.ROW_COMP_HDR_AVG'
#    rows = 1
#    cols = 1
#    srow = 0
#    scol = 0
#    data = self.tbl['ROW-COMP-HDR']['DATA']
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.ROW_COMP_HDR_SUM'
#    rows = 1
#    cols = 1
#    srow = 1
#    scol = 0
#    data = self.tbl['ROW-COMP-HDR']['DATA']
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.ROW_COMP_HDR_CNT'
#    rows = 1
#    cols = 1
#    srow = 2
#    scol = 0
#    data = self.tbl['ROW-COMP-HDR']['DATA']
#    names[name] = (rows,cols,srow,scol,data)

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.ROW_COMP_TBL'
    rows = self.tbl['ROW-COMP-TBL']['ROWS']
    cols = self.tbl['ROW-COMP-TBL']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['ROW-COMP-TBL']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    for rowIdx in range(self.tbl['ROW-COMP-TBL']['ROWS']):
      name = self._calcRangeName(fname,'ROW-COMP-TBL',rowIdx,0,'ROW-COMP-HDR')
      rows = 1
      cols = self.tbl['ROW-COMP-TBL']['COLS']
      srow = rowIdx
      scol = 0
      data = self.tbl['ROW-COMP-HDR']['DATA']
      names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    self.tbl['ROW-COMP-TBL']['NAMED-RANGES'] = names

#    name = fname + '.ROW_COMP_TBL_AVG'
#    rows = 1
#    cols = self.tbl['ROW-COMP-TBL']['COLS']
#    srow = 0
#    scol = 0
#    data = self.tbl['ROW-COMP-TBL']['DATA']
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.ROW_COMP_TBL_SUM'
#    rows = 1
#    cols = self.tbl['ROW-COMP-TBL']['COLS']
#    srow = 1
#    scol = 0
#    data = self.tbl['ROW-COMP-TBL']['DATA']
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.ROW_COMP_TBL_CNT'
#    rows = 1
#    cols = self.tbl['ROW-COMP-TBL']['COLS']
#    srow = 2
#    scol = 0
#    data = self.tbl['ROW-COMP-TBL']['DATA']
#    names[name] = (rows,cols,srow,scol,data)

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.COL_COMP_HDR'
    rows = self.tbl['COL-COMP-HDR']['ROWS']
    cols = self.tbl['COL-COMP-HDR']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['COL-COMP-HDR']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    for colIdx in range(self.tbl['COL-COMP-HDR']['COLS']):
      name = self._calcRangeName(fname,'COL-COMP-HDR',0,colIdx,'COL-COMP-HDR')
      rows = 1
      cols = 1
      srow = 0
      scol = colIdx
      data = self.tbl['COL-COMP-HDR']['DATA']
      names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    self.tbl['COL-COMP-HDR']['NAMED-RANGES'] = names

#    name = fname + '.COL_COMP_HDR_AVG'
#    rows = 1
#    cols = 1
#    srow = 0
#    scol = 0
#    data = self.tbl['COL-COMP-HDR']['DATA'][0][0]
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.COL_COMP_HDR_SUM'
#    rows = 1
#    cols = 1
#    srow = 0
#    scol = 1
#    data = self.tbl['COL-COMP-HDR']['DATA'][0][1]
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.COL_COMP_HDR_CNT'
#    rows = 1
#    cols = 1
#    srow = 0
#    scol = 2
#    data = self.tbl['COL-COMP-HDR']['DATA'][0][2]
#    names[name] = (rows,cols,srow,scol,data)

    #--------------------------------------------------------------------
    names = OrderedDict()
    name = fname + '.COL_COMP_TBL'
    rows = self.tbl['COL-COMP-TBL']['ROWS']
    cols = self.tbl['COL-COMP-TBL']['COLS']
    srow = 0
    scol = 0
    data = self.tbl['COL-COMP-TBL']['DATA']
    names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    for colIdx in range(self.tbl['COL-COMP-TBL']['COLS']):
      name = self._calcRangeName(fname,'COL-COMP-TBL',0,colIdx,'COL-COMP-HDR')
      rows = self.tbl['COL-COMP-TBL']['ROWS']
      cols = 1
      srow = 0
      scol = colIdx
      data = self.tbl['COL-COMP-TBL']['DATA']
      names[name] = MatrixData.Range(rows,cols,srow,scol,data)

    self.tbl['COL-COMP-TBL']['NAMED-RANGES'] = names

#    name = fname + '.COL_COMP_TBL_AVG'
#    rows = self.tbl['COL-COMP-TBL']['ROWS']
#    cols = 1
#    srow = 0
#    scol = 0
#    data = self.tbl['COL-COMP-TBL']['DATA'][0]
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.COL_COMP_TBL_SUM'
#    rows = self.tbl['COL-COMP-TBL']['ROWS']
#    cols = 1
#    srow = 0
#    scol = 1
#    data = self.tbl['COL-COMP-TBL']['DATA'][0]
#    names[name] = (rows,cols,srow,scol,data)
#
#    name = fname + '.COL_COMP_TBL_CNT'
#    rows = self.tbl['COL-COMP-TBL']['ROWS']
#    cols = 1
#    srow = 0
#    scol = 2
#    data = self.tbl['COL-COMP-TBL']['DATA'][0]
#    names[name] = (rows,cols,srow,scol,data)

#    self.tbl['NAMED-RANGES'] = names


