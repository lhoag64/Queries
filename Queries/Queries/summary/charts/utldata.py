import logging
from   summary.charts.chart import Chart

#----------------------------------------------------------------------
class UtlData(Chart):
  def __init__(self,matrix,region,type,period):

    self.title = 'Utilization'
    self.yAxis = 'Percent'
    self.xAxis = 'Weeks'

    self.utlCfTable = matrix[1].sheet.tables['ULT-CF']
    self.ws = self.utlCfTable[1].ws.ws
    self.utlCt = (26, 3,26,3+13)

    logging.debug('')
