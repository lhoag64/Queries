import logging
from   xlinterface.xlworkbook            import XlWorkBook
from   xlinterface.xlworksheet           import XlWorkSheet
from   summary.matrix.matrixdata         import MatrixData 
from   summary.matrix.matrixtable        import MatrixTable
from   openpyxl.chart                    import LineChart
from   openpyxl.chart                    import BarChart
from   openpyxl.chart.reference          import Reference
from   summary.matrix.actvitivydata      import ActivityData
from   summary.matrix.actvitivyamdmrdata import ActivityAmDmrData
from   summary.matrix.actvitivyammidata  import ActivityAmMiData
from   summary.matrix.ltsdata            import LtsData
from   summary.matrix.utlcfdata          import UtlCfData
from   summary.matrix.utlpsdata          import UtlPsData
from   summary.matrix.utldtdata          import UtlDtData
from   summary.matrix.utllsdata          import UtlLsData
from   summary.matrix.overtimedata       import OverTimeData
from   summary.matrix.gkadata            import GkaData
from   summary.matrix.amrkadata          import AmRkaData
from   summary.matrix.amtmcardata        import AmTmCarData
from   summary.matrix.amtmsmcdata        import AmTmSmcData
from   summary.matrix.ammirkadata        import AmMiRkaData
from   summary.matrix.actbylocdata       import ActByLocData
from   summary.matrix.actbyprdteamdata   import ActByPrdTeamData
from   summary.matrix.faeawhdata         import FaeAwhData
from   summary.matrix.faewhdata          import FaeWhData
from   summary.matrix.faeltdata          import FaeLtData
from   summary.matrix.faeotdata          import FaeOtData

#----------------------------------------------------------------------
class MetricWorkSheet:
  FuncDict = \
    {
      'FAE-AWH': FaeAwhData, \
      'FAE-WH' : FaeWhData,  \
      'FAE-LT' : FaeLtData,  \
    }
  #--------------------------------------------------------------------
  def __init__(self,ws,matrixList):
    self.ws     = ws
    self.list   = matrixList

    startRow = 2
    startCol = 2

    self.tables = {}

    for item in matrixList:
      loc    = item[0]
      region = item[1]
      mType  = item[2]
      period = item[3]
      if (mType in self.FuncDict):

        #--------------------------------------------------------------
        # Find where to put it
        #--------------------------------------------------------------
        if (loc == 'START'):
          startRow  = 2
          startCol  = 2
        elif (loc == 'RIGHT'):
          startRow += 0
          startCol  = table.rightCol + 2
        elif (loc == 'DOWN-LEFT'):
          startRow  = table.bottomRow + 2
          startCol  = 2
        elif (loc == 'DOWN'):
          startRow  = table.bottomRow + 2
          startCol += 0

        data  = self.FuncDict[mType](region,mType,period)
        table = MatrixTable(ws,startRow,startCol,data)

      else:
        logging.debug('Function table does have: ' + mType)


'''
    data  = ActivityData(region,'ACTIVITY',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ACTIVITY'] = (data,table)

    startRow += data.dataRows + 2

    data  = LtsData(region,'LTS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['LTS'] = (data,table)

    startRow += data.dataRows + 2

    data  = UtlCfData(region,'UTL-CF',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-CF'] = (data,table)

    startRow += data.dataRows + 2

    data  = UtlPsData(region,'UTL-PS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-PF'] = (data,table)

    startRow += data.dataRows + 2

    data  = UtlDtData(region,'UTL-DT',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-DT'] = (data,table)

    startRow += data.dataRows + 2

    data  = UtlLsData(region,'UTL-LS',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['ULT-LS'] = (data,table)

    startRow += data.dataRows + 2

    data  = OverTimeData(region,'OVERTIME',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['OVERTIME'] = (data,table)

    startRow += data.dataRows + 2

    data  = GkaData(region,'GKA',period)
    table = MatrixTable(ws,startRow,startCol,data)
    self.tables['GKA'] = (data,table)

    startRow += data.dataRows + 2

    if (region == 'EMEA'):
      actList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
      locList = ['UK','Sweden','Finland','France','Germany','Other (EMEA)']
      for act in actList:
        data  = ActByLocData(region,'ACT-BY-LOC',period,act=act,loc=locList)
        table = MatrixTable(ws,startRow,startCol,data)
        self.tables['ACT-' + str(act)] = (data,table)

        startRow += data.dataRows + 2

    elif (region == 'AM'):
      data  = ActivityAmDmrData(region,'ACTIVITY-AM-DMR',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['ACTIVITY-AM-DMR'] = (data,table)

      startRow += data.dataRows + 2

      data  = ActivityAmMiData(region,'ACTIVITY-AM-MI',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['ACTIVITY-AM-MI'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmRkaData(region,'AM-RKA',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-RKA'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmTmCarData(region,'AM-TM-CAR',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-TM-CAR'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmTmSmcData(region,'AM-TM-SMC',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-TM-SMC'] = (data,table)

      startRow += data.dataRows + 2

      data  = AmMiRkaData(region,'AM-MI-RKA',period)
      table = MatrixTable(ws,startRow,startCol,data)
      self.tables['AM-MI-RKA'] = (data,table)

      startRow += data.dataRows + 2

      actList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
      prdList = ['DMR','MI']
      for act in actList:
        data  = ActByPrdTeamData(region,'ACT-BY-PRD-TEAM',period,act=act,prd=prdList)
        table = MatrixTable(ws,startRow,startCol,data)
        self.tables['ACT-' + str(act)] = (data,table)

        startRow += data.dataRows + 2

    logging.debug('')
'''

