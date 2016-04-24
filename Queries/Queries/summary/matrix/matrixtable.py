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
    table = data.table

    # Set column sizes
    tRow       = startRow
    tCol       = startCol
    colDescRow = tRow
    rowDescCol = tCol
    dRows      = table.dataRows
    dCols      = table.dataCols
    cRows      = table.compRows
    cCols      = table.compCols

    # Set column sizes
    wsCol = rowDescCol
    ws.SetColWid(wsCol,table.descColWid)
    wsCol += 1
    for i in range(dCols):
      ws.SetColWid(wsCol,table.dataColWid)
      wsCol += 1

    wsRow = colDescRow
    ws.SetRowHgt(wsRow,table.descRowHgt)
    wsRow += 1
    for j in range(dRows):
      ws.SetRowHgt(wsRow,table.dataRowHgt)
      wsRow += 1

    ws.SetCell(tRow,tCol,table.title,table.titleFmt)

    wsRow = tRow + 1
    wsCol = rowDescCol
    for j in range(dRows):
      ws.SetCell(wsRow,wsCol,table.rowDesc[j],table.descColFmt)
      wsRow += 1
    for i in range(cRows):
      ws.SetCell(wsRow,wsCol,table.colCompDesc[i],table.descCompColFmt)
      wsCol += 1

    wsRow = tRow
    wsCol = tCol + 1
    for i in range(dCols):
      ws.SetCell(wsRow,wsCol,table.colDesc[i],table.descRowFmt)
      wsCol += 1
    for i in range(cCols):
      ws.SetCell(wsRow,wsCol,table.colCompDesc[i],table.descCompRowFmt)
      wsCol += 1

    wsCol = tCol + 1 
    for i in range(dCols):
      wsRow = tRow + 1
      for j in range(dRows):
        ws.SetCell(wsRow,wsCol,table.data[i][j],table.dataFmt)
        wsRow += 1
      wsCol += 1

    for i in range(len(table.compData)):
      wsRow = tRow + 1
      for j in range(len(table.compData[i])):
        ws.SetCell(wsRow,wsCol,table.compData[i][j],table.dataFmt)
        wsRow += 1
      wsCol += 1

    tRow       = startRow
    tCol       = startCol
    colDescRow = tRow
    rowDescCol = tCol
    dRows      = table.dataRows
    dCols      = table.dataCols
    cRows      = table.compRows
    cCols      = table.compCols

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