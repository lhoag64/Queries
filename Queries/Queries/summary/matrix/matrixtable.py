import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData

#----------------------------------------------------------------------
class MatrixTable:
  #--------------------------------------------------------------------
  def __init__(self,ws,startRow,startCol,matrixData):
    self.ws = ws

    data = matrixData

    # Set column sizes
    tRow       = startRow
    tCol       = startCol
    colDescRow = tRow
    rowDescCol = tCol
    dRows      = data.dataRows
    dCols      = data.dataCols
    cRows      = data.compRows
    cCols      = data.compCols

    # Set column sizes
    wsCol = rowDescCol
    ws.SetColWid(wsCol,data.descColWid)
    wsCol += 1
    for i in range(dCols):
      ws.SetColWid(wsCol,data.dataColWid)
      wsCol += 1

    wsRow = colDescRow
    ws.SetRowHgt(wsRow,data.descRowHgt)
    wsRow += 1
    for j in range(dRows):
      ws.SetRowHgt(wsRow,data.dataRowHgt)
      wsRow += 1

    ws.SetCell(tRow,tCol,data.title,data.titleFmt)

    wsRow = tRow + 1
    wsCol = rowDescCol
    for i in range(dRows):
      if (type(data.descRowFmt) is list):
        ws.SetCell(wsRow,wsCol,data.rowDesc[i],data.descRowFmt[i])
      else:
        ws.SetCell(wsRow,wsCol,data.rowDesc[i],data.descRowFmt)
      wsRow += 1
    for i in range(cRows):
      if (type(data.descCompRowFmt) is list):
        ws.SetCell(wsRow,wsCol,data.colCompDesc[i],data.descCompRowFmt[i])
      else:
        ws.SetCell(wsRow,wsCol,data.colCompDesc[i],data.descCompRowFmt)
      wsCol += 1

    wsRow = tRow
    wsCol = tCol + 1
    for i in range(dCols):
      if (type(data.descColFmt) is list):
        ws.SetCell(wsRow,wsCol,data.colDesc[i],data.descColFmt[i])
      else:
        ws.SetCell(wsRow,wsCol,data.colDesc[i],data.descColFmt)
      wsCol += 1
    for i in range(cCols):
      if (type(data.descCompColFmt) is list):
        ws.SetCell(wsRow,wsCol,data.colCompDesc[i],data.descCompColFmt[i])
      else:
        ws.SetCell(wsRow,wsCol,data.colCompDesc[i],data.descCompColFmt)
      wsCol += 1

    wsCol = tCol + 1 
    for i in range(dCols):
      wsRow = tRow + 1
      for j in range(dRows):
        ws.SetCell(wsRow,wsCol,data.data[i][j],data.dataFmt)
        wsRow += 1
      wsCol += 1

    for i in range(len(data.compData)):
      wsRow = tRow + 1
      for j in range(len(data.compData[i])):
        ws.SetCell(wsRow,wsCol,data.compData[i][j],data.dataFmt)
        wsRow += 1
      wsCol += 1

    tRow       = startRow
    tCol       = startCol
    colDescRow = tRow
    rowDescCol = tCol
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


    logging.debug('')