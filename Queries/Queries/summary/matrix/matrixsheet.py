import logging
from   xlinterface                import WrkBook
from   xlinterface                import WrkSheet
from   summary.matrix.metricsheet import MetricSheet
from   summary.matrix.faesheet    import FaeSheet

#----------------------------------------------------------------------
class MatrixSheet:
  def __init__(self,ws,region,type,period):
    self.ws = ws
    self.region = region
    self.type   = type
    self.period = type

    if (type == 'METRICS'):
      self.sheet = MetricSheet(ws,region,type,period)
    if (type == 'FAE'):
      self.sheet = FaeSheet(ws,region,type,period)

    logging.debug('')
#    else:
#      self.sheet = FaeSheet(ws,region,type,period)


