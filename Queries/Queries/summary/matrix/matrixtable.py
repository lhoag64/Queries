import logging
from   collections                import OrderedDict
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData
# Conditional formatting
from openpyxl                     import Workbook
from openpyxl.styles              import Color,PatternFill,Font,Border
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule     import ColorScaleRule,CellIsRule,FormulaRule,IconSet,FormatObject,Rule

#----------------------------------------------------------------------
class TableItem:
  def __init__(self,sRow,sCol,data):
    self.sRow = sRow
    self.sCol = sCol
    self.eRow = sRow + data['ROWS'] - 1
    self.eCol = sCol + data['COLS'] - 1
    self.rows = data['ROWS']
    self.cols = data['COLS']
    self.hgt  = data['HGT']
    self.wid  = data['WID']
    self.data = data['DATA']
    self.fmt  = data['FMT']

#----------------------------------------------------------------------
class MatrixTable:
  #--------------------------------------------------------------------
  def __init__(self,ws,sRow,sCol,data):

    dRows = data['TBL-DATA']['ROWS']
    dCols = data['TBL-DATA']['COLS']

    items = OrderedDict()
    items['TITLE'       ] = TableItem(sRow+0        ,sCol+0        ,data['TITLE'])
    items['ROW-DATA-HDR'] = TableItem(sRow+1        ,sCol+0        ,data['ROW-DATA-HDR'])
    items['COL-DATA-HDR'] = TableItem(sRow+0        ,sCol+1        ,data['COL-DATA-HDR'])
    items['TBL-DATA'    ] = TableItem(sRow+1        ,sCol+1        ,data['TBL-DATA'])
    items['ROW-COMP-HDR'] = TableItem(sRow+1+dRows+0,sCol+0        ,data['ROW-COMP-HDR'])
    items['ROW-COMP-TBL'] = TableItem(sRow+1+dRows+0,sCol+1        ,data['ROW-COMP-TBL'])
    items['COL-COMP-HDR'] = TableItem(sRow+0        ,sCol+1+dCols+0,data['COL-COMP-HDR'])
    items['COL-COMP-TBL'] = TableItem(sRow+1        ,sCol+1+dCols+0,data['COL-COMP-TBL'])

    self.items = items
    self.data  = data
    self.name  = data['NAME']
    self.ws    = ws

    title = ' '.join(data['TITLE']['DATA'][0][0].split('\r'))
    logging.debug('Creating ' + title.ljust(80) + ' ' + str(sRow).rjust(3) + ' ' + str(sCol).rjust(3))

    rowDataHdrCols = data['COL-DATA-HDR']['COLS']
    colDataHdrRows = data['COL-DATA-HDR']['ROWS']
    rowCompHdrRows = data['ROW-COMP-HDR']['ROWS']
    rowCompTblRows = data['ROW-COMP-TBL']['ROWS']
    colCompTblCols = data['COL-COMP-TBL']['COLS']
    tblDataRows    = data['TBL-DATA'    ]['ROWS']
    tblDataCols    = data['TBL-DATA'    ]['COLS']

    self.topRow    = sRow
    self.bottomRow = sRow + colDataHdrRows + tblDataRows + rowCompTblRows
    self.leftCol   = sCol
    self.rightCol  = sCol + rowDataHdrCols + tblDataCols + colCompTblCols

    # Set column sizes
    rowDataHdrWid  = data['ROW-DATA-HDR']['WID']
    tblDataWid     = data['TBL-DATA'    ]['WID']
    colCompTblWid  = data['COL-COMP-TBL']['WID']

    wsCol = sCol
    ws.SetColWid(wsCol,rowDataHdrWid)
    wsCol += 1
    for colIdx in range(tblDataCols):
      ws.SetColWid(wsCol,tblDataWid)
      wsCol += 1
    for colIdx in range(colCompTblCols):
      ws.SetColWid(wsCol,colCompTblWid)
      wsCol += 1

    # Set row sizes
    colDataHdrHgt  = data['COL-DATA-HDR']['HGT']
    tblDataHgt     = data['TBL-DATA'    ]['HGT']
    rowCompHdrHgt  = data['ROW-COMP-HDR']['HGT']

    wsRow = sRow
    ws.SetRowHgt(wsRow,colDataHdrHgt)
    wsRow += 1
    for rowIdx in range(tblDataRows):
      ws.SetRowHgt(wsRow,tblDataHgt)
      wsRow += 1
    for rowIdx in range(rowCompHdrRows):
      ws.SetRowHgt(wsRow,rowCompHdrHgt)
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
            ws.SetCell(wsRow+rowIdx,wsCol+colIdx,item.data[rowIdx][colIdx],fmt)
          else:
            if (type(item.fmt) is list):
              fmt = item.fmt[rowIdx][colIdx]
            if (type(fmt) is dict):
              if ('I' in fmt):
                fmt = fmt['I']
              if ('F' in fmt):
                fmt = fmt['F']
            ws.SetCell(wsRow+rowIdx,wsCol+colIdx,item.data[rowIdx][colIdx],fmt)

    for name in items:
      item = items[name]
      ws.DrawBorder(item.sRow,item.sCol,item.eRow,item.eCol, 'medium')


  #--------------------------------------------------------------------
#  for item in 

    # Create named ranges
#    pyws = ws.ws
#    pywb = ws.wb
#    name = self.name
#
#    self.rowCompRanges = []
#    sRow = self.rowCompTbl.sRow
#    sCol = self.rowCompTbl.sCol
#    eRow = self.rowCompTbl.eRow
#    eCol = self.rowCompTbl.eCol
##    for row in range(self.rowCompHdr.rows):
##      name = self.name + '_' + self.colCompHdr.data[row].upper()
##      self.rowCompRanges.append(ws.AddNamedRange(name,sRow,sCol,eRow,eCol))
##      sRow += 1
##      eRow += 1
#
#    self.colCompRanges = []
#    sRow = self.colCompTbl.sRow
#    sCol = self.colCompTbl.sCol
#    eRow = self.colCompTbl.eRow
#    eCol = self.colCompTbl.eCol
##    for col in range(self.colCompHdr.cols):
##      name = self.name + '_' + self.colCompHdr.data[col].upper()
##      self.colCompRanges.append(ws.AddNamedRange(name,sRow,sCol,eRow,eCol))
##      sRow += 1
##      eRow += 1
#
##    for item in self.matrixData.rangeList:
##      logging.debug('')


