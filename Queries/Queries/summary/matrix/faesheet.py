import logging
from   xlinterface    import WrkBook
from   xlinterface    import WrkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable

#----------------------------------------------------------------------
class FaeSheet:
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 2
    startCol = 2

    data  = MatrixData(region,'FAE-AWH',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2



