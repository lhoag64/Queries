import logging
from   xlinterface.xlworkbook             import XlWorkBook
from   xlinterface.xlworksheet            import XlWorkSheet
from   summary.matrix.metricworksheet     import MetricWorkSheet
#from   summary.matrix.faeworksheet        import FaeWorkSheet
from   summary.summary.metricsummarysheet import MetricSummarySheet
from   summary.summary.faesummarysheet    import FaeSummarySheet
from   summary.charts.metricchartsheet    import MetricChartSheet
from   summary.charts.faechartsheet       import FaeChartSheet

#----------------------------------------------------------------------
class SummaryWorkBook:
  def __init__(self):
    self.wsDict = {}
    self.wb = XlWorkBook()
    ws = self.wb.GetActiveSheet()
    self.wb.SetName(ws,'Summary')
    self.wsDict['Summary'] = ws

  #--------------------------------------------------------------------
  def AddMatrixSheet(self,wsName,matrixList):

    ws = self.wb.CreateXlWorkSheet(wsName)
    matrix = MetricWorkSheet(ws,matrixList)
    self.wsDict[wsName] = ('Matrix',matrix,ws,wsName)

  #--------------------------------------------------------------------
  def AddCharts(self,region,type,period):
    shName = region + '-' + type + '-' + period + '-CHARTS'

    if (period == 'ALL'):
      p = 'YTD'
    else:
      p = '???'

    if (type == 'METRICS'):
      name = 'Graphs (' + region + '-' + p + ')'
    elif (type == 'FAE'):
      name = 'Graphs (FAE-' + region + '-' + p + ')'
    else:
      name = '???'

    ws = self.wb.CreateXlWorkSheet(name)
    if (type == 'METRICS'):
      charts = MetricChartSheet(ws,region,type,period)
    elif (type == 'FAE'):
      charts = FaeChartSheet(ws,region,type,period)
    self.wsDict[shName] = ('Charts',charts,ws,name)

  #--------------------------------------------------------------------
  def AddSummary(self,region,type,period):
    shName = region + '-' + type + '-' + period + '-SUMMARY'

    if (period == 'ALL'):
      p = 'YTD'
    else:
      p = period

    if (type == 'METRICS'):
      name = 'Summary (' + region + '-' + p + ')'
    elif (type == 'FAE'):
      name = 'Summary (FAE-' + region + '-' + p + ')'
    else:
      name = '???'

    ws = self.wb.CreateXlWorkSheet(name)
    if (type == 'METRICS'):
      summary = MetricSummarySheet(ws,region,type,period)
    elif (type == 'FAE'):
      summary = FaeSummarySheet(ws,region,type,period)
    self.wsDict[shName] = ('Summary',summary,ws,name)

  #--------------------------------------------------------------------
#  def AddCharts(self,region,type,period):
#    shName = region + '-' + type + '-' + period + '-CHARTS'
#
#    if (period == 'ALL'):
#      p = 'YTD'
#    else:
#      p = '???'
#
#    if (type == 'METRICS'):
#      name = 'Graphs (' + region + '-' + p + ')'
#    elif (type == 'FAE'):
#      name = 'Graphs (FAE-' + region + '-' + p + ')'
#    else:
#      name = '???'
#
#    stxt = shName.split('-')
#    text = stxt[0] + '-' + stxt[1] + '-' + stxt[2] + '-' + 'MATRIX'
#    if (text not in self.wsDict):
#      logging.error('No worksheet named: ' + text)
#
#    cs = self.wb.CreateXlChrtSheet(name)
#    charts = ChartsSheet(cs,self.wsDict[text],region,type,period)
#    self.wsDict[shName] = ('Charts',charts,cs,name)
    
  #--------------------------------------------------------------------
  def Order(self):
    self.wb.RemoveSheetByName('Summary')

  #--------------------------------------------------------------------
  def Save(self,filename):
    self.wb.Save(filename)
