import logging
from   xlinterface.xlworkbook     import XlWorkBook
from   xlinterface.xlworksheet    import XlWorkSheet
from   summary.matrix.matrixdata  import MatrixData 
from   summary.matrix.matrixtable import MatrixTable
from   database.database          import Database as Db
# Conditional formatting
from openpyxl                     import Workbook
from openpyxl.styles              import Color,PatternFill,Font,Border
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule     import ColorScaleRule,CellIsRule,FormulaRule,IconSet,FormatObject,Rule

#----------------------------------------------------------------------
class FaeSummarySheet:
  def __init__(self,ws,region,type,period):
    self.ws     = ws
    self.region = region
    self.type   = type
    self.period = period

    #startRow = 200
    #startCol = 200

    #data  = MatrixData(region,'FAE-AWH',period)
    #table = MatrixTable(ws,startRow,startCol,data)
    #startRow += data.table.dataRows + 2

    #data  = MatrixData(region,'FAE-WH',period)
    #table = MatrixTable(ws,startRow,startCol,data)
    #startRow += data.table.dataRows + 2

    #data  = MatrixData(region,'FAE-LT',period)
    #table = MatrixTable(ws,startRow,startCol,data)
    #startRow += data.table.dataRows + 2

    #data  = MatrixData(region,'FAE-OT',period)
    #table = MatrixTable(ws,startRow,startCol,data)
    #startRow += data.table.dataRows + 2

    self.drawSummary(region,type,period)

#----------------------------------------------------------------------
  def drawSummary(self,region,type,period):

    c1 = FormatObject(type='min',gte='0',val= 0.0)
    c2 = FormatObject(type='num',gte='0',val=45.0)
    c3 = FormatObject(type='num',gte='0',val=50.0)
    iSet = IconSet(iconSet='3TrafficLights1',showValue=True,reverse=True,cfvo=[c1,c2,c3])
    rule = Rule(type='iconSet',iconSet=iSet)

    self.ws.SetColWid(2,10)
    self.ws.SetColWid(3,30)
    self.ws.SetColWid(4,10)
    self.ws.SetColWid(5,25)
    self.ws.SetColWid(6,25)
    self.ws.SetColWid(7,10)
    self.ws.SetRowHgt(5,55)

    self.ws.ws.merge_cells('C3:F3')


    fmt1  = {'hAlign':'C','vAlign':'C','font':{'emph':'B','size':14}}
    fmt2  = {'hAlign':'C','vAlign':'C','wrap':True,'border':{'A':'thin'},'fill':'Blue 2','font':{'emph':'B'}}

    weeks = Db.WeeksTbl.GetWeeks(Db.db,period)
    data  = Db.TsEntryTbl.GetFaeHourSummary(Db.db,region,weeks)

    rows = len(data)
    erow = 2+rows+6

    self.ws.DrawRegion(2,2,erow,7,'thick','Blue 1')

    title = 'Summary Statement: '
    if (period == 'ALL'):
      title += 'Year To Date (YTD)'
    else:
      if (period in ['JAN','FEB','MAR','APR','MAY','JUN']):
        title += period

    self.ws.SetCell( 3, 3,'Monthly Summary Statement: Year To Date (YTD)',fmt1)
    self.ws.SetCell( 5, 4,'Region',fmt2)
    self.ws.SetCell( 5, 5,'Average hours worked\r&\rEU WTD Status',fmt2)
    self.ws.SetCell( 5, 6,'Average additional hours',fmt2)

    wsRow = 6
    wsCol = 3
    for item in data:
      name = item[0]
      avg  = item[1]
      ot   = item[2]
      nrm  = item[3]
      max  = item[4]
      lbr  = item[5]
      rgn  = item[6]
      if (lbr == 'P'):
        color = 'Green 1'
      else:
        color = 'Yellow 1'
      fmt1 = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':color}
      fmt2 = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':color}
      fmt3 = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':color,'numFmt':'0.0'}
      self.ws.SetCell(wsRow,wsCol+0,name,fmt1)
      self.ws.SetCell(wsRow,wsCol+1,rgn,fmt2)
      self.ws.SetCell(wsRow,wsCol+2,avg,fmt3)
      self.ws.SetCell(wsRow,wsCol+3,ot ,fmt3)

      wsRow += 1

    rng = 'E' + str(6) + ':E' + str(6+rows)
    self.ws.ws.conditional_formatting.add(rng,rule)

    fmt1 = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    self.ws.SetCell(erow+3,wsCol+0,'Internal member of staff',fmt1)
    fmt1 = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    self.ws.SetCell(erow+4,wsCol+0,'Contractor',fmt1)

    logging.debug('')

