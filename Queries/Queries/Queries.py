import logging
import os
from   logconfig                   import LogConfig
from   database                    import Database as Db
from   timesheet.calendar          import Calendar
from   timesheet.faeteam           import FaeTeam
from   timesheet.fldata            import FlData
from   timesheet.tsdata            import TsData
#from   summary.wbinfo              import WbInfo
from   summary.wbdata              import WbData
#from   summary.summary.summarydata import SummaryData
#from   summary.summaryworkbook     import SummaryWorkBook

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

  Db(r'X:\Reporting\Timesheets','timesheets.db')

  if (False):
    InitializeDatabaseTables()
    InitializeTimesheetTables()

  wbData = WbData()

  amList =                                                                                          \
    [                                                                                               \
      ((' 0',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACTIVITY'     ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','LTS'          ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','UTL-CF'       ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','UTL-PS'       ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','UTL-DT'       ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','UTL-LS'       ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','LTYPE'        ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','GKA'          ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'10',{'ACT':10})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'11',{'ACT':11})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'12',{'ACT':12})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'13',{'ACT':13})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'14',{'ACT':14})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'15',{'ACT':15})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'16',{'ACT':16})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'17',{'ACT':17})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'18',{'ACT':18})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'19',{'ACT':19})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'20',{'ACT':20})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'21',{'ACT':21})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'22',{'ACT':22})  ,  \
      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC'   ,'23',{'ACT':23})  ,  \
      ((' 0',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','ALL','FAE-AWH'      ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','ALL','FAE-WH'       ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','ALL','FAE-OT'       ,None,None)        ,  \
      (('+1',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','ALL','LTYPE'        ,None,None)        ,  \
      ((' 0',' 0'),'SUMMARY EMEA YTD'   ,'SUMMARY','AM'  ,'YTD','STD'          ,None,None)         \
    ]                                                                                     \

  wbData.AddList(amList)
  wbData.Process()

  wbData.Order()
  wbData.Save('FAE AM MATRIX.xlsx')

  logging.debug('End of Program')

#      ((' 0',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','LTYPE'     ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','FAE-OT'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','FAE-WH'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','FAE-AWH'   ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','10',{'ACT':10}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','10',{'ACT':10}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','11',{'ACT':11}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','12',{'ACT':12}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','13',{'ACT':13}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','14',{'ACT':14}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','GKA'       ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACTIVITY'  ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','LTS'       ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','UTL-CF'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','UTL-PS'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','UTL-DT'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','UTL-LS'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','UTL-CF'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','UTL-PS'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','UTL-DT'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','UTL-LS'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','UTL-OT'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','10',{'ACT':10}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','11',{'ACT':11}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','12',{'ACT':12}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','13',{'ACT':13}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','14',{'ACT':14}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','15',{'ACT':15}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','16',{'ACT':16}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','17',{'ACT':17}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','18',{'ACT':18}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','19',{'ACT':19}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','20',{'ACT':20}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','21',{'ACT':21}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','22',{'ACT':22}),  \
#      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','23',{'ACT':23}),  \
#      ((' 0',' 0'),'ALL FAE YTD'  ,'MATRIX' ,'ALL' ,'ALL','FAE-WH'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL FAE YTD'  ,'MATRIX' ,'ALL' ,'ALL','FAE-AWH'   ,None,None)      ,  \
#      (('+1',' 0'),'ALL FAE YTD'  ,'MATRIX' ,'ALL' ,'ALL','FAE-LT'    ,None,None)      ,  \
#      (('+1',' 0'),'ALL FAE YTD'  ,'MATRIX' ,'ALL' ,'ALL','FAE-OT'    ,None,None)      ,  \
#      ((' 0',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACTIVITY'  ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','LTS'       ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','UTL-CF'    ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','UTL-PS'    ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','UTL-DT'    ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','UTL-LS'    ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','OVERTIME'  ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','GKA'       ,None,None)      ,  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','10',{'ACT':10}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','11',{'ACT':11}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','12',{'ACT':12}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','13',{'ACT':13}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','14',{'ACT':14}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','15',{'ACT':15}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','16',{'ACT':16}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','17',{'ACT':17}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','18',{'ACT':18}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','19',{'ACT':19}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','20',{'ACT':20}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','21',{'ACT':21}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','22',{'ACT':22}),  \
#      (('+1',' 0'),'AM YTD'       ,'MATRIX' ,'AM'  ,'ALL','ACT-BY-LOC','23',{'ACT':23}),  \
#      ((' 0',' 0'),'AM FAE YTD'   ,'MATRIX' ,'AM'  ,'ALL','FAE-WH'    ,None,None)      ,  \
#      (('+1',' 0'),'AM FAE YTD'   ,'MATRIX' ,'AM'  ,'ALL','FAE-AWH'   ,None,None)      ,  \
#      (('+1',' 0'),'AM FAE YTD'   ,'MATRIX' ,'AM'  ,'ALL','FAE-LT'    ,None,None)      ,  \
#      (('+1',' 0'),'AM FAE YTD'   ,'MATRIX' ,'AM'  ,'ALL','FAE-OT'    ,None,None)      ,  \
#      ((' 0',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACTIVITY'  ,None,None)      ,  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','LTS'       ,None,None)      ,  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','UTL-CF'    ,None,None)      ,  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','UTL-PS'    ,None,None)      ,  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','UTL-DT'    ,None,None)      ,  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','UTL-LS'    ,None,None)      ,  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','10',{'ACT':10}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','11',{'ACT':11}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','12',{'ACT':12}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','13',{'ACT':13}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','14',{'ACT':14}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','15',{'ACT':15}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','16',{'ACT':16}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','17',{'ACT':17}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','18',{'ACT':18}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','19',{'ACT':19}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','20',{'ACT':20}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','21',{'ACT':21}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','22',{'ACT':22}),  \
#      (('+1',' 0'),'AM APR'       ,'MATRIX' ,'AM'  ,'APR','ACT-BY-LOC','23',{'ACT':23}),  \
#      ((' 0',' 0'),'AM FAE APR'   ,'MATRIX' ,'AM'  ,'APR','FAE-WH'    ,None,None)      ,  \
#      (('+1',' 0'),'AM FAE APR'   ,'MATRIX' ,'AM'  ,'APR','FAE-AWH'   ,None,None)      ,  \
#      (('+1',' 0'),'AM FAE APR'   ,'MATRIX' ,'AM'  ,'APR','FAE-LT'    ,None,None)      ,  \
#      (('+1',' 0'),'AM FAE APR'   ,'MATRIX' ,'AM'  ,'APR','FAE-OT'    ,None,None)      ,  \
#      ((' 0',' 0'),'AM SUMMRY YTD','SUMMARY','AM'  ,'YTD','STD'       ,None,None)         \
#    ]

  