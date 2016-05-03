import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable 
from   summary.matrix.faeawhdata  import FaeAwhData
from   summary.matrix.faewhdata   import FaeWhData
from   summary.matrix.faeltdata   import FaeLtData
from   summary.matrix.faeotdata   import FaeOtData

#----------------------------------------------------------------------
class FaeWorkSheet:
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 2
    startCol = 2

    data  = FaeAwhData(region,'FAE-AWH',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.dataRows + 2

    data  = FaeWhData(region,'FAE-WH',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.dataRows + 2

    data  = FaeLtData(region,'FAE-LT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.dataRows + 2

    data  = FaeOtData(region,'FAE-OT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.dataRows + 2



