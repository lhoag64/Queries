import logging
from   xlinterface                import WrkBook
from   xlinterface                import WrkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable

#----------------------------------------------------------------------
class MetricSheet:
  #--------------------------------------------------------------------
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 2
    startCol = 2

    data  = MatrixData(region,'ACTIVITY',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'LTS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-CF',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-PS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-DT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-LS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'OVERTIME',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'GKA',period)
    table = MatrixTable(ws,startRow,startCol,data)
    startRow += data.table.dataRows + 2

    actList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    locList = ['UK','Sweden','Finland','France','Germany','Other (EMEA)']
    for act in actList:
      data  = MatrixData(region,'ACT-BY-LOC',period,act=act,loc=locList)
      table = MatrixTable(ws,startRow,startCol,data)
      startRow += data.table.dataRows + 2


    logging.debug('')


