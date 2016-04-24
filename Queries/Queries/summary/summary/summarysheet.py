import logging
from   xlinterface.xlworkbook             import XlWorkBook
from   xlinterface.xlworksheet            import XlWorkSheet
from   summary.matrix.matrixdata          import MatrixData 
from   summary.matrix.matrixtable         import MatrixTable
from   summary.summary.metricsummarysheet import MetricSummarySheet
from   summary.summary.faesummarysheet    import FaeSummarySheet

#----------------------------------------------------------------------
class SummarySheet:
  def __init__(self,ws,region,type,period):
    self.ws = ws
    self.region = region
    self.type   = type
    self.period = period

    if (type == 'METRICS'):
      self.sheet = MetricSummarySheet(ws,region,type,period)
    if (type == 'FAE'):
      self.sheet = FaeSummarySheet(ws,region,type,period)

    logging.debug('')