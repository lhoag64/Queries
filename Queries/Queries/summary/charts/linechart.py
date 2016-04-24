import logging
import openpyxl
from   openpyxl.chart import LineChart as pxlxLineChart
from   openpyxl.chart import Reference

#----------------------------------------------------------------------
class LineChart:
  def __init__(self,cs,data):

    ch = pxlxLineChart()
    ch.title = data.chart.title
    ch.style = 13
#    ch.y_axis = data.chart.yAxis
 #   ch.x_axis = data.chart.xAxis

    ws = data.chart.ws

    data = Reference(ws,min_row=26,min_col=3,max_row=26,max_col=3+13)
    ch.add_data(data,from_rows=True)

    cs.cs.add_chart(ch)

    logging.debug('')
