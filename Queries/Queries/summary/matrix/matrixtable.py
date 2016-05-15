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
class MatrixTableArea:
  def __init__(self,startRow,startCol,data):
    self.sRow = startRow
    self.sCol = startCol
    self.eRow = startRow + data.rows - 1
    self.eCol = startCol + data.cols - 1
    self.rows = data.rows
    self.cols = data.cols
    self.hgt  = data.hgt
    self.wid  = data.wid
    self.data = data.data
    self.fmt  = data.fmt

#----------------------------------------------------------------------
class MatrixTable:
  #--------------------------------------------------------------------
  def __init__(self,ws,startRow,startCol,data):
    self.ws = ws

    self.name        = data.name
    self.title       = MatrixTableArea(startRow+0,startCol+0,data.title)
    self.rowHdr      = MatrixTableArea(startRow+1,startCol+0,data.rowHdr)
    self.colHdr      = MatrixTableArea(startRow+0,startCol+1,data.colHdr)
    self.data        = MatrixTableArea(startRow+1,startCol+1,data.data)
    self.rowCompHdr  = MatrixTableArea(startRow+1+self.data.rows,startCol+0,data.rowCompHdr)
    self.rowCompData = MatrixTableArea(startRow+1+self.data.rows,startCol+1,data.rowCompData)
    self.colCompHdr  = MatrixTableArea(startRow+0,startCol+1+self.data.cols,data.colCompHdr)
    self.colCompData = MatrixTableArea(startRow+1,startCol+1+self.data.cols,data.colCompData)

    title = self.title.data.split('\r')
    title = ' '.join(title)
    logging.debug('Creating ' + title.ljust(80) + ' ' + str(startRow).rjust(3) + ' ' + str(startCol).rjust(3))

    self.topRow    = startRow
    self.bottomRow = startRow + self.colHdr.rows + self.data.rows + self.rowCompData.rows
    self.leftCol   = startCol
    self.rightCol  = startCol + self.rowHdr.cols + self.data.cols + self.colCompData.cols

    # Set column sizes
    wsCol = startCol
    ws.SetColWid(wsCol,self.rowHdr.wid)
    wsCol += 1
    for i in range(self.data.cols):
      ws.SetColWid(wsCol,self.data.wid)
      wsCol += 1
    for i in range(self.colCompData.cols):
      ws.SetColWid(wsCol,self.colCompData.wid)
      wsCol += 1

    # Set row sizes
    wsRow = startRow
    ws.SetRowHgt(wsRow,self.colHdr.hgt)
    wsRow += 1
    for j in range(self.data.rows):
      ws.SetRowHgt(wsRow,self.data.hgt)
      wsRow += 1
    for j in range(self.rowCompData.rows):
      ws.SetRowHgt(wsRow,self.rowCompData.hgt)
      wsRow += 1

    # Draw title
    title = self.title
    ws.SetCell(title.sRow,title.sCol,title.data,title.fmt)

    # Draw row descriptions
    rowHdr = self.rowHdr
    wsRow = rowHdr.sRow
    wsCol = rowHdr.sCol
    for i in range(rowHdr.rows):
      if (type(rowHdr.fmt) is list):
        ws.SetCell(wsRow,wsCol,rowHdr.data[i],rowHdr.fmt[i])
      else:
        ws.SetCell(wsRow,wsCol,rowHdr.data[i],rowHdr.fmt)
      wsRow += 1

    # Draw row computed descriptions
    rowCompHdr = self.rowCompHdr
    wsRow = rowCompHdr.sRow
    wsCol = rowCompHdr.sCol
    for i in range(rowCompHdr.rows):
      if (type(rowCompHdr.fmt) is list):
        ws.SetCell(wsRow,wsCol,rowCompHdr.data[i],rowCompHdr.fmt[i])
      else:
        ws.SetCell(wsRow,wsCol,rowCompHdr.data[i],rowCompHdr.fmt)
      wsRow += 1


    # Draw col descriptions
    colHdr = self.colHdr
    wsRow = colHdr.sRow
    wsCol = colHdr.sCol
    for i in range(colHdr.cols):
      if (type(colHdr.fmt) is list):
        ws.SetCell(wsRow,wsCol,colHdr.data[i],colHdr.fmt[i])
      else:
        ws.SetCell(wsRow,wsCol,colHdr.data[i],colHdr.fmt)
      wsCol += 1

    # Draw col computed descriptions
    colCompHdr = self.colCompHdr
    wsRow = colCompHdr.sRow
    wsCol = colCompHdr.sCol
    for i in range(colCompHdr.cols):
      if (type(colCompHdr.fmt) is list):
        ws.SetCell(wsRow,wsCol,colCompHdr.data[i],colCompHdr.fmt[i])
      else:
        ws.SetCell(wsRow,wsCol,colCompHdr.data[i],colCompHdr.fmt)
      wsCol += 1

    # Draw data
    data = self.data
    wsRow = data.sRow
    wsCol = data.sCol
    for i in range(data.cols):
      wsRow = data.sRow
      for j in range(data.rows):
        ws.SetCell(wsRow,wsCol,data.data[i][j],data.fmt)
        wsRow += 1
      wsCol += 1

    # Draw row computed data
    data = self.rowCompData
    wsRow = data.sRow
    wsCol = data.sCol
    if (type(data.data) is list):
      for i in range(data.cols):
        wsRow = data.sRow
        if (type(data.data[i]) is list):
          for j in range(data.rows):
            ws.SetCell(wsRow,wsCol,data.data[i][j],data.fmt)
            wsRow += 1
        else:
          ws.SetCell(wsRow,wsCol,data.data[i],data.fmt)
        wsCol += 1


    # Draw col computed data
    data = self.colCompData
    wsRow = data.sRow
    wsCol = data.sCol
    if (data.cols == 1):
      wsRow = data.sRow
      for i in range(data.rows):
        ws.SetCell(wsRow,wsCol,data.data[i],data.fmt)
        wsRow += 1
    else:
      for i in range(data.cols):
        wsRow = data.sRow
        for j in range(data.rows):
          ws.SetCell(wsRow,wsCol,data.data[i][j],data.fmt)
          wsRow += 1
        wsCol += 1

    ws.DrawBorder(self.title.sRow,      self.title.sCol,      self.title.eRow,      self.title.eCol,      'medium')
    ws.DrawBorder(self.rowHdr.sRow,     self.rowHdr.sCol,     self.rowHdr.eRow,     self.rowHdr.eCol,     'medium')
    ws.DrawBorder(self.colHdr.sRow,     self.colHdr.sCol,     self.colHdr.eRow,     self.colHdr.eCol,     'medium')
    ws.DrawBorder(self.data.sRow,       self.data.sCol,       self.data.eRow,       self.data.eCol,       'medium')
    ws.DrawBorder(self.rowCompHdr.sRow, self.rowCompHdr.sCol, self.rowCompHdr.eRow, self.rowCompHdr.eCol, 'medium')
    ws.DrawBorder(self.rowCompData.sRow,self.rowCompData.sCol,self.rowCompData.eRow,self.rowCompData.eCol,'medium')
    ws.DrawBorder(self.colCompHdr.sRow, self.colCompHdr.sCol, self.colCompHdr.eRow, self.colCompHdr.eCol, 'medium')
    ws.DrawBorder(self.colCompData.sRow,self.colCompData.sCol,self.colCompData.eRow,self.colCompData.eCol,'medium')

    # Create named ranges
    pyws = ws.ws
    pywb = ws.wb
    name = self.name

    self.rowCompRanges = []
    sRow = self.rowCompData.sRow
    sCol = self.rowCompData.sCol
    eRow = self.rowCompData.eRow
    eCol = self.rowCompData.eCol
    for row in range(self.rowCompHdr.rows):
      name = self.name + '_' + self.colCompHdr.data[row].upper()
      self.rowCompRanges.append(ws.AddNamedRange(name,sRow,sCol,eRow,eCol))
      sRow += 1
      eRow += 1

    self.colCompRanges = []
    sRow = self.colCompData.sRow
    sCol = self.colCompData.sCol
    eRow = self.colCompData.eRow
    eCol = self.colCompData.eCol
    for col in range(self.colCompHdr.cols):
      name = self.name + '_' + self.colCompHdr.data[col].upper()
      self.colCompRanges.append(ws.AddNamedRange(name,sRow,sCol,eRow,eCol))
      sRow += 1
      eRow += 1




