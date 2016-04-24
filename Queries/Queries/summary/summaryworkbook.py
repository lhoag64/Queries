import logging
from   xlinterface.xlworkbook       import XlWorkBook
from   xlinterface.xlworksheet      import XlWorkSheet
from   summary.matrix.matrixsheet   import MatrixSheet
from   summary.charts.chartssheet   import ChartsSheet
from   summary.summary.summarysheet import SummarySheet

#----------------------------------------------------------------------
class SummaryWorkBook:
  def __init__(self):
    self.wsDict = {}
    self.wb = XlWorkBook()
    ws = self.wb.GetActiveSheet()
    self.wb.SetName(ws,'Summary')
    self.wsDict['Summary'] = ws

  #--------------------------------------------------------------------
  def AddMatrix(self,region,type,period):
    shName = region + '-' + type + '-' + period + '-MATRIX'

    if (period == 'ALL'):
      p = 'YTD'
    else:
      p = '???'

    if (type == 'METRICS'):
      name = 'Matrix (' + region + '-' + p + ')'
    elif (type == 'FAE'):
      name = 'Matrix (FAE-' + region + '-' + p + ')'
    else:
      name = '???'

    ws = self.wb.CreateXlWorkSheet(name)
    matrix = MatrixSheet(ws,region,type,period)
    self.wsDict[shName] = ('Matrix',matrix,ws,name)

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
    matrix = ChartsSheet(ws,region,type,period)
    self.wsDict[shName] = ('Charts',matrix,ws,name)

  #--------------------------------------------------------------------
  def AddSummary(self,region,type,period):
    shName = region + '-' + type + '-' + period + '-SUMMARY'

    if (period == 'ALL'):
      p = 'YTD'
    else:
      p = '???'

    if (type == 'METRICS'):
      name = 'Summary (' + region + '-' + p + ')'
    elif (type == 'FAE'):
      name = 'Summary (FAE-' + region + '-' + p + ')'
    else:
      name = '???'

    ws = self.wb.CreateXlWorkSheet(name)
    matrix = SummarySheet(ws,region,type,period)
    self.wsDict[shName] = ('Summary',matrix,ws,name)

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
  def Save(self,filename):
    self.wb.Save(filename)
