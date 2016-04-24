import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable

#----------------------------------------------------------------------
class FaeSummarySheet:
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 200
    startCol = 200

    data  = MatrixData(region,'FAE-AWH',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'FAE-WH',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'FAE-LT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'FAE-OT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2



