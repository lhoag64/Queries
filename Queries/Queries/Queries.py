import logging
import os
from   logconfig               import LogConfig
from   database                import Database as Db
from   timesheet.calendar      import Calendar
from   timesheet.faeteam       import FaeTeam
from   timesheet.fldata        import FlData
from   timesheet.tsdata        import TsData
from   summary.summaryworkbook import SummaryWorkBook

#----------------------------------------------------------------------
def InitializeDatabaseTables():

  tblList = []
  tblList.append('fae_lbrtype')
  tblList.append('fae_loc')
  tblList.append('fae_prdtm')
  tblList.append('fae_region')
  tblList.append('fae_team')
  tblList.append('ts_code')
  tblList.append('ts_loc')
  tblList.append('ts_act')
  tblList.append('ts_prd')
  tblList.append('ts_lts')
  tblList.append('ts_file')
  tblList.append('ts_entry')
  tblList.append('weeks')

  Db.CreateTables(tblList)

#----------------------------------------------------------------------
def InitializeTimesheetTables():

  Calendar(2016)

  rng = range(1,51+1)

  emea_team = FaeTeam('EMEA')
  am_team   = FaeTeam('AM')
  gc_team   = FaeTeam('GC')

  fldata = FlData(r'X:\Reporting\Timesheets\EMEA',emea_team)
  tsdata = TsData('EMEA',emea_team,rng,fldata)
  Db.InsertTimesheets(tsdata)

  fldata = FlData(r'X:\Reporting\Timesheets\AM',am_team)
  tsdata = TsData('AM',am_team,rng,fldata)
  Db.InsertTimesheets(tsdata)

  fldata = FlData(r'X:\Reporting\Timesheets\GC',gc_team)
  tsdata = TsData('GC',gc_team,rng,fldata)
  Db.InsertTimesheets(tsdata)

#----------------------------------------------------------------------
if (__name__ == '__main__'):

  os.chdir('X:\Reporting\Timesheets')

  LogConfig('queries.log')
  logging.debug('Start of Program')

  Db()
  Db.Connect(r'X:\Reporting\Timesheets','timesheets.db')

  if (False):
    InitializeDatabaseTables()
    InitializeTimesheetTables()

  #emeaActList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
  #amActList   = emeaActList
  #gcActList   = emeaActList
  #emeaLocList = ['UK','Sweden','Finland','France','Germany','OTH']
  #emeaOthList = ['Poland','Portugal','Spain','Ireland','Turkey']
  #amLocList   = ['East','West','Canada','Latin America','South America']

  matrixList = []
 
  options = {'ACT':10}
  matrixList.append(('START'   ,'ALL','ACT-BY-LOC','ALL',options))
  for i in range(10,23+1):
    options = {'ACT':i}
    matrixList.append(('DOWN','EMEA','ACT-BY-LOC','ALL',options))
     
  matrixList.append(('DOWN'    ,'EMEA','GKA'       ,'ALL',None))
  matrixList.append(('DOWN'    ,'EMEA','OVERTIME'  ,'ALL',None))
  matrixList.append(('DOWN'    ,'EMEA','UTL-DT'    ,'ALL',None))
  matrixList.append(('DOWN'    ,'EMEA','UTL-LS'    ,'ALL',None))
  matrixList.append(('DOWN'    ,'EMEA','UTL-PS'    ,'ALL',None))
  matrixList.append(('DOWN'    ,'EMEA','UTL-CF'    ,'ALL',None))
  matrixList.append(('DOWN'    ,'EMEA','LTS'       ,'ALL',None))
  #matrixList.append(('DOWN',     'ALL',       'ACTIVITY', 'ALL'))
  #matrixList.append(('DOWN',     'EMEA',      'ACTIVITY', 'APR'))
  #matrixList.append(('DOWN',     'ALL',       'FAE-OT',   'ALL'))
  #matrixList.append(('DOWN',     'ALL',       'FAE-LT',   'ALL'))
  #matrixList.append(('DOWN',     'AM',        'FAE-AWH',  'ALL'))
  #matrixList.append(('RIGHT',    'AM',        'FAE-WH',   'ALL'))
  #matrixList.append(('DOWN-LEFT','EMEA',      'FAE-AWH',  'ALL'))
  #matrixList.append(('RIGHT',    'EMEA',      'FAE-WH',   'ALL'))
  #matrixList.append(('DOWN-LEFT','GC',        'FAE-AWH',  'ALL'))
  #matrixList.append(('RIGHT',    'GC',        'FAE-WH',   'ALL'))
  #matrixList.append(('DOWN',     ['AM','GC'], 'FAE-AWH',  'JAN'))
  #matrixList.append(('DOWN',     ['AM','GC'], 'FAE-AWH',  'FEB'))

  summary = SummaryWorkBook()
  summary.AddMatrixSheet('FAE Examples',matrixList)

  summary.Order()

  summary.Save('test.xlsx')


  logging.debug('End of Program')