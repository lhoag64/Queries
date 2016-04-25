import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable
from   summary.charts.chartdata   import ChartData
from   openpyxl.chart             import LineChart
from   openpyxl.chart             import BarChart
from   openpyxl.chart             import PieChart
from   openpyxl.chart.reference   import Reference

#----------------------------------------------------------------------
class MetricSummarySheet:
  #--------------------------------------------------------------------
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    startRow = 200
    startCol = 200

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

    self.drawSummary()
    #self.drawActChart()

  #--------------------------------------------------------------------
  def drawSummary(self):
    self.ws.SetColWid(2,10)
    self.ws.SetColWid(3,60)
    self.ws.SetColWid(4,20)
    self.ws.SetColWid(5,20)
    self.ws.SetColWid(6,10)

    self.ws.DrawRegion(2,2,66,6,'thick','Blue 1')

    self.ws.ws.merge_cells('C3:E3')

    fmt1  = {'hAlign':'C','vAlign':'C','font':{'emph':'B','size':14}}
    fmt2  = {'hAlign':'C','vAlign':'C','wrap':True,'border':{'A':'thin'},'fill':'Blue 2','font':{'emph':'B'}}

    fmt2a = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 2','font':{'emph':'B','size':11}}
    fmt2b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 2','numFmt':'0.0','font':{'emph':'B'}}
    fmt3  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3'}
    fmt3a = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3'}
    fmt3b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3','numFmt':'0.0','font':{'emph':'B'}}
    fmt4  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    fmt4b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Green 1','numFmt':'0.0','font':{'emph':'B'}}
    fmt5  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1'}
    fmt5b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1','numFmt':'0.0','font':{'emph':'B'}}
    fmt6  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Red 1'}
    fmt6b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Red 1','numFmt':'0.0','font':{'emph':'B'}}
    fmt7  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Yellow 1'}
    fmt7b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Yellow 1','numFmt':'0.0','font':{'emph':'B'}}

    self.ws.SetCell( 3, 3,'Monthly Summary Statement: Year To Date (YTD)',fmt1)

    self.ws.SetCell( 5, 4,'Average hours worked & EU WTD Status',fmt2)
    self.ws.SetCell( 5, 5,'Average additional hours',fmt2)


#    self.ws.DrawBorder( 6, 3, 10, 5,'medium')
#    self.ws.DrawBorder( 6, 3,  6, 5,'medium')
#    self.ws.DrawBorder(12, 3, 16, 5,'medium')
#    self.ws.DrawBorder(12, 3, 12, 5,'medium')
#    self.ws.DrawBorder(19, 3, 35, 5,'medium')
#    self.ws.DrawBorder(19, 3, 19, 5,'medium')
#    self.ws.DrawBorder(37, 3, 44, 5,'medium')
#    self.ws.DrawBorder(37, 3, 37, 5,'medium')
#    self.ws.DrawBorder(46, 3, 49, 5,'medium')
#    self.ws.DrawBorder(46, 3, 46, 5,'medium')


#    ltsChart = PieChart()
#    data   = Reference(self.ws.ws,min_col=5,min_row=47,max_row=49)
#    labels = Reference(self.ws.ws,min_col=3,min_row=47,max_row=49)
#    ltsChart.add_data(data)
#    ltsChart.set_categories(labels)
#    ltsChart.title = 'Labour Vs Travel'
#    self.ws.ws.add_chart(ltsChart,'H46')

  #--------------------------------------------------------------------
#  def drawActChart(self):
#
#    chart = BarChart()
#    chart.title = 'Activites'
#
#    row1 = 200
#    row2 = 214
#    col1 = self.ws.GetColumnIndex('GR')
#    col2 = self.ws.GetColumnIndex('HF')
#
#    data = Reference(self.ws.ws,min_row=row1,min_col=col1,max_row=row2,max_col=col2)
#    chart.add_data(data)
#
#    chart.type     = 'col'
#    chart.style    =   12
#    chart.grouping = 'stacked'
#    chart.overlap  = 100
#
#    self.ws.ws.add_chart(chart,'B17')

