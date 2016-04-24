import logging
from   xlinterface.xlworkbook         import XlWorkBook
from   xlinterface.xlworksheet        import XlWorkSheet
from   summary.matrix.metricworksheet import MetricWorkSheet
from   summary.matrix.faeworksheet    import FaeWorkSheet

#----------------------------------------------------------------------
class MatrixSheet:
  def __init__(self,ws,region,type,period):
    self.ws = ws
    self.region = region
    self.type   = type
    self.period = period

    if (type == 'METRICS'):
      self.sheet = MetricWorkSheet(ws,region,type,period)
    if (type == 'FAE'):
      self.sheet = FaeWorkSheet(ws,region,type,period)

    logging.debug('')
#    else:
#      self.sheet = FaeSheet(ws,region,type,period)


