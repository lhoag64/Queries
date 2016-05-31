import logging
from   collections                       import OrderedDict
from   xlinterface.xlworkbook            import XlWorkBook
from   xlinterface.xlworksheet           import XlWorkSheet
from   summary.matrix.matrixdata         import MatrixData 
from   openpyxl.chart                    import LineChart
from   openpyxl.chart                    import PieChart
from   openpyxl.chart.reference          import Reference 
from   openpyxl.chart.series             import Series

#----------------------------------------------------------------------
class TableItem:
  def __init__(self,sRow,sCol,data):
    self.sRow  = sRow
    self.sCol  = sCol
    self.eRow  = sRow + data['ROWS'] - 1
    self.eCol  = sCol + data['COLS'] - 1
    self.rows  = data['ROWS']
    self.cols  = data['COLS']
    self.hgt   = data['HGT']
    self.wid   = data['WID']
    self.data  = data['DATA']
    self.fmt   = data['FMT']
    if ('NAMED-RANGES' in data):
      self.names = data['NAMED-RANGES']
    else:
      self.names = None

#----------------------------------------------------------------------
class ChartTable:
  def __init__(self,ws,sheet,sRow,sCol,item,nameDict):

    self.sheet    = sheet
    self.ws       = ws
    self.item     = item
    self.data     = item.data
    self.name     = item.data['NAME']
    self.startRow = sRow
    self.startCol = sCol

    data = item.data

    dRows = data['TBL-DATA']['ROWS']
    dCols = data['TBL-DATA']['COLS']

    items = OrderedDict()
    items['TITLE'       ] = TableItem(sRow+0        ,sCol+0        ,data['TITLE'       ])
    items['ROW-DATA-HDR'] = TableItem(sRow+1        ,sCol+0        ,data['ROW-DATA-HDR'])
    items['COL-DATA-HDR'] = TableItem(sRow+0        ,sCol+1        ,data['COL-DATA-HDR'])
    items['TBL-DATA'    ] = TableItem(sRow+1        ,sCol+1        ,data['TBL-DATA'    ])

    self.items = items
    self.names = OrderedDict()

    title = ' '.join(data['TITLE']['DATA'][0][0].split('\r'))
    logging.debug('Creating ' + title.ljust(80) + ' ' + str(sRow).rjust(3) + ' ' + str(sCol).rjust(3))

    rowDataHdrCols = data['COL-DATA-HDR']['COLS']
    colDataHdrRows = data['COL-DATA-HDR']['ROWS']
    tblDataRows    = data['TBL-DATA'    ]['ROWS']
    tblDataCols    = data['TBL-DATA'    ]['COLS']

    self.topRow    = sRow
    self.bottomRow = sRow + colDataHdrRows + tblDataRows
    self.leftCol   = sCol
    self.rightCol  = sCol + rowDataHdrCols + tblDataCols

    # Set column sizes
    rowDataHdrWid  = data['ROW-DATA-HDR']['WID']
    tblDataWid     = data['TBL-DATA'    ]['WID']

    wsCol = sCol
    ws.SetColWid(wsCol,rowDataHdrWid)
    wsCol += 1
    for colIdx in range(tblDataCols):
      ws.SetColWid(wsCol,tblDataWid)
      wsCol += 1

    # Set row sizes
    colDataHdrHgt  = data['COL-DATA-HDR']['HGT']
    tblDataHgt     = data['TBL-DATA'    ]['HGT']

    wsRow = sRow
    ws.SetRowHgt(wsRow,colDataHdrHgt)
    wsRow += 1
    for rowIdx in range(tblDataRows):
      ws.SetRowHgt(wsRow,tblDataHgt)
      wsRow += 1

    for name in items:
      item = items[name]

      wsRow = item.sRow
      wsCol = item.sCol
      for rowIdx in range(item.rows):
        for colIdx in range(item.cols):
          fmt   = item.fmt
          if (item.data[rowIdx][colIdx] != None):
            if (type(item.fmt) is list):
              fmt = item.fmt[rowIdx][colIdx]
            if (type(fmt) is dict):
              if (type(item.data[rowIdx][colIdx]) is int):
                if ('I' in fmt):
                  fmt = fmt['I']
              if (type(item.data[rowIdx][colIdx]) is float):
                if ('F' in fmt):
                  fmt = fmt['F']
              if ('G' in fmt):
                fmt = fmt['G']
            ws.SetCell(wsRow+rowIdx,wsCol+colIdx,item.data[rowIdx][colIdx],fmt)
          else:
            if (type(item.fmt) is list):
              fmt = item.fmt[rowIdx][colIdx]
            if (type(fmt) is dict):
              if ('I' in fmt):
                fmt = fmt['I']
              if ('F' in fmt):
                fmt = fmt['F']
              if ('G' in fmt):
                fmt = fmt['G']
            ws.SetCell(wsRow+rowIdx,wsCol+colIdx,item.data[rowIdx][colIdx],fmt)

    for name in items:
      item = items[name]
      ws.DrawBorder(item.sRow,item.sCol,item.eRow,item.eCol, 'medium')

#    for name in items:
#      item = items[name]
#      if (item.names != None):
#        for namedRange in item.names:
#          self._createNamedRange(namedRange,item)


