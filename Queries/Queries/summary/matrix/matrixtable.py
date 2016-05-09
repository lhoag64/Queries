import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData

#----------------------------------------------------------------------
class MatrixTableArea:
  def __init__(self,startRow,startCol,data):
    self.sRow = startRow
    self.sCol = startCol
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

    self.title       = MatrixTableArea(startRow+0,startCol+0,data.title)
    self.rowHdr      = MatrixTableArea(startRow+1,startCol+0,data.rowHdr)
    self.colHdr      = MatrixTableArea(startRow+0,startCol+1,data.colHdr)
    self.data        = MatrixTableArea(startRow+1,startCol+1,data.data)
    self.rowCompHdr  = MatrixTableArea(startRow+1+self.data.rows,startCol+0,data.rowCompHdr)
    self.rowCompData = MatrixTableArea(startRow+1+self.data.rows,startCol+1,data.rowCompData)
    self.colCompHdr  = MatrixTableArea(startRow+0,startCol+1+self.data.cols,data.colCompHdr)
    self.colCompData = MatrixTableArea(startRow+1,startCol+1+self.data.cols,data.colCompData)

    self.topRow    = startRow
    self.bottomRow = startRow + self.colHdr.rows + self.data.rows + self.rowCompData.rows
    self.leftCol   = startCol
    self.rightCol  = startCol + self.rowHdr.cols + self.data.cols + self.colCompData.rows

    # Set column sizes
    wsCol = startCol
    ws.SetColWid(wsCol,self.rowHdr.wid)
    wsCol += 1
    for i in range(self.data.cols):
      ws.SetColWid(wsCol,self.data.wid)
      wsCol += 1

    # Set column sizes
    wsRow = startRow
    ws.SetRowHgt(wsRow,self.colHdr.hgt)
    wsRow += 1
    for j in range(self.data.rows):
      ws.SetRowHgt(wsRow,self.data.hgt)
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

'''
    # Draw col descriptions
    colHdr = self.colHdr
    wsRow = colHdr.sRow
    wsCol = colHdr.sCol
    for i in range(colHdr.cols):
      if (type(colHdr.fmt) is list):
        ws.SetCell(wsRow,wsCol,colHdr.data[i],colHdr.fmt[i])
      else:
        ws.SetCell(wsRow,wsCol,colHdr.data[i],colHdr.fmt)
      wsRow += 1

    # Draw col computed descriptions
    colCompHdr = self.colCompHdr
    wsRow = colCompHdr.sRow
    wsCol = colCompHdr.sCol
    for i in range(colCompHdr.cols):
      if (type(colCompHdr.fmt) is list):
        ws.SetCell(wsRow,wsCol,colCompHdr.data[i],colCompHdr.fmt[i])
      else:
        ws.SetCell(wsRow,wsCol,colCompHdr.data[i],colCompHdr.fmt)
      wsRow += 1


    # Draw data
    data = self.data
    wsRow = data.sRow
    wsCol = data.sCol
    for i in range(data.cols):
      wsRow = data.sRow + 1
      for j in range(data.rows):
        ws.SetCell(wsRow,wsCol,data.data[i][j],data.fmt)
        wsRow += 1
      wsCol += 1

    # Draw row computed data
    rowCompData = self.rowCompData
    wsRow = rowCompData.sRow
    wsCol = rowCompData.sCol
    for i in range(rowCompData.cols):
      wsRow = rowCompData.sRow + 1
      for j in range(len(data.rowpData[i])):
        ws.SetCell(wsRow,wsCol,rowCompData.data[i][j],rowCompData.fmt)
        wsRow += 1
      wsCol += 1

    # Draw col computed data
    colCompData = self.colCompData
    wsRow = colCompData.sRow
    wsCol = colCompData.sCol
    for i in range(colCompData.cols):
      wsRow = colCompData.sRow + 1
      for j in range(len(data.compData[i])):
        ws.SetCell(wsRow,wsCol,colCompData.data[i][j],colCompData.fmt)
        wsRow += 1
      wsCol += 1

    tRow       = startRow
    tCol       = startCol
    colHdr = tRow
    rowHdr = tCol
    dRows      = data.dataRows
    dCols      = data.dataCols
    cRows      = data.compRows
    cCols      = data.compCols

    # Around the whole thing
    leftCol   = tCol
    rightCol  = tCol+dCols+cCols
    topRow    = tRow
    bottomRow = tRow + dRows
    ws.DrawBorder(topRow,leftCol,bottomRow,rightCol,'medium')

    self.fullDim = (topRow,leftCol,bottomRow,rightCol)

    # Across the top
    leftCol   = tCol
    rightCol  = tCol+dCols+cCols
    topRow    = tRow
    bottomRow = tRow
    ws.DrawBorder(topRow,leftCol,bottomRow,rightCol,'medium')

    self.topDescDim = (topRow,leftCol+1,bottomRow,rightCol)

    # Along the left side
    leftCol   = tCol
    rightCol  = tCol
    topRow    = tRow
    bottomRow = tRow + dRows
    ws.DrawBorder(topRow,leftCol,bottomRow,rightCol,'medium')

    self.leftDescDim = (topRow+1,leftCol,bottomRow,rightCol)

    # Along the right side
    leftCol   = tCol+1+dCols
    rightCol  = tCol+dCols+cCols
    topRow    = tRow
    bottomRow = tRow + dRows
    ws.DrawBorder(topRow,leftCol,bottomRow,rightCol,'medium')

    topRow   = tRow
    botRow   = tRow + dRows + cRows
    leftCol  = tCol
    rightCol = tCol + dCols + cCols
'''
