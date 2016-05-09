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

    table = MatrixTable(ws,startRow,startCol,FaeAwhData(region,'FAE-AWH',period))
    startRow += table.bottomRow

    table = MatrixTable(ws,startRow,startCol,FaeWhData(region,'FAE-WH',period))
    startRow += table.bottomRow

#    table = MatrixTable(ws,startRow,startCol,FaeLtData(region,'FAE-LT',period))
#    startRow += table.bottomRow
#
#    table = MatrixTable(ws,startRow,startCol,FaeOtData(region,'FAE-OT',period))
#    startRow += table.bottomRow



