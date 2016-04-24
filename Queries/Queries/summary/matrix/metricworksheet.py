import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable

#----------------------------------------------------------------------
class MetricWorkSheet:
  #--------------------------------------------------------------------
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 2
    startCol = 2

    self.tables = {}


    data  = MatrixData(region,'ACTIVITY',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ACTIVITY'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'LTS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['LTS'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-CF',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-CF'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-PS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-PF'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-DT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-DT'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'UTL-LS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-LS'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'OVERTIME',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['OVERTIME'] = (data,table)

    startRow += data.table.dataRows + 2

    data  = MatrixData(region,'GKA',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['GKA'] = (data,table)

    startRow += data.table.dataRows + 2

    actList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    locList = ['UK','Sweden','Finland','France','Germany','Other (EMEA)']
    for act in actList:
      data  = MatrixData(region,'ACT-BY-LOC',period,act=act,loc=locList)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['ACT-' + str(act)] = (data,table)

      startRow += data.table.dataRows + 2


    logging.debug('')


