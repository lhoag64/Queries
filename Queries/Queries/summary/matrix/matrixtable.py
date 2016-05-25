import logging
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
    self.ws = ws

    dRows = data['TBL-DATA']['ROWS']
    dCols = data['TBL-DATA']['COLS']

    self.matrixData = data
    self.name       = data['NAME']
    self.title      = TableItem(sRow+0        ,sCol+0        ,data['TITLE'])
    self.rowDataHdr = TableItem(sRow+1        ,sCol+0        ,data['ROW-DATA-HDR'])
    self.colDataHdr = TableItem(sRow+0        ,sCol+1        ,data['COL-DATA-HDR'])
    self.tblData    = TableItem(sRow+1        ,sCol+1        ,data['TBL-DATA'])
    self.rowCompHdr = TableItem(sRow+1+dRows+0,sCol+0        ,data['ROW-COMP-HDR'])
    self.rowCompTbl = TableItem(sRow+1+dRows+0,sCol+1        ,data['ROW-COMP-TBL'])
    self.colCompHdr = TableItem(sRow+0        ,sCol+1+dCols+0,data['COL-COMP-HDR'])
    self.colCompTbl = TableItem(sRow+1        ,sCol+1+dCols+0,data['COL-COMP-TBL'])

    title = self.title.data[0][0].split('\r')
    title = ' '.join(title)
    logging.debug('Creating ' + title.ljust(80) + ' ' + str(sRow).rjust(3) + ' ' + str(sCol).rjust(3))

    self.topRow    = sRow
    self.bottomRow = sRow + self.colDataHdr.rows + self.tblData.rows + self.rowCompTbl.rows
    self.leftCol   = sCol
    self.rightCol  = sCol + self.rowDataHdr.cols + self.tblData.cols + self.colCompTbl.cols

    # Set column sizes
    wsCol = sCol
    ws.SetColWid(wsCol,self.rowDataHdr.wid)
    wsCol += 1
    for colIdx in range(self.tblData.cols):
      ws.SetColWid(wsCol,self.tblData.wid)
      wsCol += 1
    for colIdx in range(self.colCompTbl.cols):
      ws.SetColWid(wsCol,self.colCompTbl.wid)
      wsCol += 1

    # Set row sizes
    wsRow = sRow
    ws.SetRowHgt(wsRow,self.colDataHdr.hgt)
    wsRow += 1
    for rowIdx in range(self.tblData.rows):
      ws.SetRowHgt(wsRow,self.tblData.hgt)
      wsRow += 1
    for rowIdx in range(self.rowCompHdr.rows):
      ws.SetRowHgt(wsRow,self.rowCompHdr.hgt)
      wsRow += 1

    itemList =            \
      [                   \
        self.title     ,  \
        self.rowDataHdr,  \
        self.colDataHdr,  \
        self.tblData   ,  \
        self.rowCompHdr,  \
        self.rowCompTbl,  \
        self.colCompHdr,  \
        self.colCompTbl   \
      ]

    for item in itemList:
      wsRow = item.sRow
      wsCol = item.sCol
      fmt   = item.fmt
      for rowIdx in range(item.rows):
        for colIdx in range(item.cols):
          if (type(item.fmt) is list):
            fmt = item.fmt[rowIdx]
          if (item.data != None):
            ws.SetCell(wsRow+rowIdx,wsCol+colIdx,item.data[rowIdx][colIdx],fmt)

    for item in itemList:
      ws.DrawBorder(item.sRow,item.sCol,item.eRow,item.eCol, 'medium')

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


