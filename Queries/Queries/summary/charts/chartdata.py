import logging
from   summary.charts.utldata import UtlData

#----------------------------------------------------------------------
class ChartData:
  def __init__(self,matrix,region,type,period):
    self.region = region
    self.type   = type
    self.period = period
    self.table  = None

    if (type == 'UTIL'):
      self.chart = UtlData(matrix,region,type,period)


