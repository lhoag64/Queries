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
  #rng = range(1,1+1)

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

#  Db.tsdb.db.close()

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

  matrixList = []
  matrixList.append(('START',    'ALL',       'FAE-LT', 'ALL'))
  matrixList.append(('DOWN',     'AM',        'FAE-AWH','ALL'))
  matrixList.append(('RIGHT',    'AM',        'FAE-WH', 'ALL'))
  matrixList.append(('DOWN-LEFT','EMEA',      'FAE-AWH','ALL'))
  matrixList.append(('RIGHT',    'EMEA',      'FAE-WH', 'ALL'))
  matrixList.append(('DOWN-LEFT','GC',        'FAE-AWH','ALL'))
  matrixList.append(('RIGHT',    'GC',        'FAE-WH', 'ALL'))
  matrixList.append(('DOWN',     ['AM','GC'], 'FAE-AWH','JAN'))

  summary = SummaryWorkBook()
  summary.AddMatrixSheet('FAE Examples',matrixList)

#  matrixList = []
#  matrixList.append(('START',    'AM',  'FAE-AWH','JAN'))
#  matrixList.append(('RIGHT',    'AM',  'FAE-WH', 'JAN'))
#  matrixList.append(('DOWN-LEFT','EMEA','FAE-AWH','JAN'))
#  matrixList.append(('RIGHT',    'EMEA','FAE-WH', 'JAN'))
#  matrixList.append(('DOWN-LEFT','GC',  'FAE-AWH','JAN'))
#  matrixList.append(('RIGHT',    'GC',  'FAE-WH', 'JAN'))
#  summary.AddMatrixSheet('JAN FAE Tables by Region',matrixList)
#  matrixList = []
#  matrixList.append(('START',    'AM',  'FAE-AWH','FEB'))
#  matrixList.append(('RIGHT',    'AM',  'FAE-WH', 'FEB'))
#  matrixList.append(('DOWN-LEFT','EMEA','FAE-AWH','FEB'))
#  matrixList.append(('RIGHT',    'EMEA','FAE-WH', 'FEB'))
#  matrixList.append(('DOWN-LEFT','GC',  'FAE-AWH','FEB'))
#  matrixList.append(('RIGHT',    'GC',  'FAE-WH', 'FEB'))
#  summary.AddMatrixSheet('FEB FAE Tables by Region',matrixList)
#  matrixList = []
#  matrixList.append(('START',    'AM',  'FAE-AWH','MAR'))
#  matrixList.append(('RIGHT',    'AM',  'FAE-WH', 'MAR'))
#  matrixList.append(('DOWN-LEFT','EMEA','FAE-AWH','MAR'))
#  matrixList.append(('RIGHT',    'EMEA','FAE-WH', 'MAR'))
#  matrixList.append(('DOWN-LEFT','GC',  'FAE-AWH','MAR'))
#  matrixList.append(('RIGHT',    'GC',  'FAE-WH', 'MAR'))
#  summary.AddMatrixSheet('MAR FAE Tables by Region',matrixList)
#  matrixList = []
#  matrixList.append(('START',    'AM',  'FAE-AWH','APR'))
#  matrixList.append(('RIGHT',    'AM',  'FAE-WH', 'APR'))
#  matrixList.append(('DOWN-LEFT','EMEA','FAE-AWH','APR'))
#  matrixList.append(('RIGHT',    'EMEA','FAE-WH', 'APR'))
#  matrixList.append(('DOWN-LEFT','GC',  'FAE-AWH','APR'))
#  matrixList.append(('RIGHT',    'GC',  'FAE-WH', 'APR'))
#  summary.AddMatrixSheet('APR FAE Tables by Region',matrixList)

#  matrixList = [JAN]
#  matrixList.append(('AM',  'FAE-AWH','FEB'))
#  matrixList.append(('EMEA','FAE-AWH','FEB'))
#  matrixList.append(('GC',  'FAE-AWH','FEB'))
#  summary.AddMatrixSheet('FEB FAE Tables by Region',matrixList)
#  matrixList = []
#  matrixList.append(('AM',  'FAE-AWH','MAR'))
#  matrixList.append(('EMEA','FAE-AWH','MAR'))
#  matrixList.append(('GC',  'FAE-AWH','MAR'))
#  summary.AddMatrixSheet('MAR FAE Tables by Region',matrixList)
#  matrixList = []
#  matrixList.append(('AM',  'FAE-AWH','APR'))
#  matrixList.append(('EMEA','FAE-AWH','APR'))
#  matrixList.append(('GC',  'FAE-AWH','APR'))
#  summary.AddMatrixSheet('APR FAE Tables by Region',matrixList)
  #summary.AddMatrix('EMEA','FAE','ALL')
  #summary.AddSummary('AM','METRICS','ALL')
  #summary.AddSummary('AM','FAE','ALL')
  #summary.AddMatrix('AM','METRICS','ALL')
  #summary.AddMatrix('AM','FAE','ALL')
  #summary.AddCharts('AM','METRICS','ALL')
  #summary.AddCharts('AM','FAE','ALL')
#  summary.AddMatrix('AM','METRICS','FEB')
#  summary.AddMatrix('GC','METRICS','JAN')
#  summary.AddMatrix('ALL','FAE','JAN')
#  summary.AddCharts('EMEA','METRICS','MAR')
#  summary.AddCharts('EMEA','FAE','ALL')
#  summary.AddSummary('EMEA','METRICS','ALL')
#  summary.AddMatrix('ALL','METRICS','ALL')
#  summary.AddMatrix('ALL','FAE','ALL')
  #summary.AddMatrix('EMEA','FAE','ALL')
  #summary.AddCharts('EMEA','FAE','ALL')

  summary.Order()

  summary.Save('test.xlsx')


  #CreateWeeksTable(db) 
  #Activity(db) 
  #LvT(db)
  #UtilizationCF(db)
  #UtilizationLS(db)
  #Overtime(db)

  logging.debug('End of Program')

#  fae_lbrtype - key,desc
#  fae_loc - key,desc
#  fae_prdteam - key,desc
#  fae_region - key,desc
#  fae_team - fullname,fname,fnalias,lname,lnalias,region,lbr_type,prd_team,fae_loc,norm_hours,max_hours,start_date,end_date
#  wbs_code - code,desc,downtime,leave
#  location - location,desc
#  product - product,desc
#  activity - activity,desc,billable,pre_sales,non_billable
#  timesheets - name,fname,lname,region,lbr_type,prd_team,fae_loc,wc_date,entry_date,wbs_code,work_loc,activity,product,hours,work_type,notes,ts_name,ts_date,ts_file
#  work_type - key,desc
#  ts_file - file,desc