import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   openpyxl.chart             import BarChart
from   openpyxl.chart.reference          import Reference
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable 
#from   summary.matrix.faeawhdata  import FaeAwhData
#from   summary.matrix.faewhdata   import FaeWhData
#from   summary.matrix.faeltdata   import FaeLtData
#from   summary.matrix.faeotdata   import FaeOtData

#----------------------------------------------------------------------
class FaeChartSheet:
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 200
    startCol = 200

#    data  = FaeAwhData(region,'FAE-AWH',period)
#    table = MatrixTable(ws,startRow,startCol,data)
#    startRow += data.dataRows + 2
#
#    data  = FaeWhData(region,'FAE-WH',period)
#    table = MatrixTable(ws,startRow,startCol,data)
#    startRow += data.dataRows + 2
#
#    data  = FaeLtData(region,'FAE-LT',period)
#    table = MatrixTable(ws,startRow,startCol,data)
#    startRow += data.dataRows + 2
#
#    data  = FaeOtData(region,'FAE-OT',period)
#    table = MatrixTable(ws,startRow,startCol,data)
#    startRow += data.dataRows + 2

    self.drawOtChart()
#    self.drawLtrChart()

  #--------------------------------------------------------------------
  def drawOtChart(self):

    chart = BarChart()
    chart.type = 'col'
    chart.style = 10
    chart.title = 'Additional Hours'
    chart.y_axis.title = 'Hours'
    chart.x_axis.title = 'Weeks'
    mincol = self.ws.GetColumnIndex('GS')
    maxcol = self.ws.GetColumnIndex('HE')
    data = Reference(self.ws.ws,min_row=242,min_col=mincol,max_row=259,max_col=maxcol)
    chart.add_data(data)

    self.ws.ws.add_chart(chart,'B2')

