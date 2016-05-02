import logging
from   logconfig               import LogConfig
from   database                import Database as Db
from   timesheet.calendar      import Calendar
from   timesheet.faeteam       import FaeTeam
from   timesheet.fldata        import FlData
from   timesheet.tsdata        import TsData
from   summary.summaryworkbook import SummaryWorkBook

#----------------------------------------------------------------------
def InitializeDatabase():
  Db()
  Db.Connect(r'X:\Reporting\Timesheets','timesheets.db')

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
def InitializeTimesheetData():

  Calendar(2016)

  rng = range(1,16+1)
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

  LogConfig('queries.log')
  logging.debug('Start of Program')

  InitializeDatabase()
  InitializeTimesheetData()

  summary = SummaryWorkBook()
  #summary.AddMatrix('EMEA','METRICS','JAN')
  summary.AddSummary('AM','METRICS','ALL')
  summary.AddSummary('AM','FAE','ALL')
  summary.AddMatrix('AM','METRICS','ALL')
  summary.AddMatrix('AM','FAE','ALL')
  summary.AddCharts('AM','METRICS','ALL')
  summary.AddCharts('AM','FAE','ALL')
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