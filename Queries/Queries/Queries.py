import logging
import os
from   logconfig               import LogConfig
from   database                import Database as Db
from   timesheet.calendar      import Calendar
from   timesheet.faeteam       import FaeTeam
from   timesheet.fldata        import FlData
from   timesheet.tsdata        import TsData
from   summary.summarydata     import SummaryData
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

  Db(r'X:\Reporting\Timesheets','timesheets.db')

  if (False):
    InitializeDatabaseTables()
    InitializeTimesheetTables()

  logging.debug('------------------------------------------')
  logging.debug('------------------------------------------')
  logging.debug('------------------------------------------')
  logging.debug('AM ---------------------------------------')
  logging.debug('------------------------------------------')
  logging.debug('------------------------------------------')
  logging.debug('------------------------------------------')

  summaryWb   = SummaryWorkBook()
  summaryData = SummaryData(summaryWb)

  amList =                                                                                \
    [                                                                                     \
      ((' 0',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','FAE-AWH'   ,None,None)      ,  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACT-BY-LOC','10',{'ACT':10}),  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','10',{'ACT':10}),  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','11',{'ACT':11}),  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','12',{'ACT':12}),  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','13',{'ACT':13}),  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'EMEA','ALL','ACT-BY-LOC','14',{'ACT':14}),  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','GKA'       ,None,None)      ,  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','ACTIVITY'  ,None,None)      ,  \
      (('+1',' 0'),'ALL YTD'      ,'MATRIX' ,'ALL' ,'ALL','LTS'       ,None,None)      ,  \
    ]                                                                                     \
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

  summaryData.AddList(amList)
  summaryData.Process()

  summaryWb.Order()
  summaryWb.Save('FAE AM MATRIX.xlsx')

#  logging.debug('------------------------------------------')
#  logging.debug('------------------------------------------')
#  logging.debug('------------------------------------------')
#  logging.debug('ALL --------------------------------------')
#  logging.debug('------------------------------------------')
#  logging.debug('------------------------------------------')
#  logging.debug('------------------------------------------')
#
#  summary = SummaryWorkBook()
#
#  matrixList = []
#  matrixList.append(('START'    ,'ALL' ,'ACTIVITY'  ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'LTS'       ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-CF'    ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-PS'    ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-DT'    ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-LS'    ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'OVERTIME'  ,'ALL',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'GKA'       ,'ALL',None))
#  for i in range(10,23+1):
#    options = {'ACT':i}
#    matrixList.append(('DOWN','ALL' ,'ACT-BY-LOC','ALL',options))
#
#  summary.AddMatrixSheet('GLOBAL YTD',matrixList)
#
#  matrixList = []
#  matrixList.append(('START'    ,'ALL' ,'FAE-WH'    ,'ALL',None))
#  matrixList.append(('RIGHT'    ,'ALL' ,'FAE-AWH'   ,'ALL',None))
#  matrixList.append(('DOWN-LEFT','ALL' ,'FAE-LT'    ,'ALL',None))
#  matrixList.append(('RIGHT'    ,'ALL' ,'FAE-OT'    ,'ALL',None))
#
#  summary.AddMatrixSheet('GLOBAL FAE YTD',matrixList)
#
#  matrixList = []
#  matrixList.append(('START'    ,'ALL' ,'ACTIVITY'  ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'LTS'       ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-CF'    ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-PS'    ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-DT'    ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-LS'    ,'JAN',None))
#
#  for i in range(10,23+1):
#    options = {'ACT':i}
#    matrixList.append(('DOWN'     ,'ALL' ,'ACT-BY-LOC','JAN',options))
#
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-WH'    ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-AWH'   ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-LT'    ,'JAN',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-OT'    ,'JAN',None))
#
#  summary.AddMatrixSheet('GLOBAL JAN',matrixList)
#
#  matrixList = []
#  matrixList.append(('START'    ,'ALL' ,'ACTIVITY'  ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'LTS'       ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-CF'    ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-PS'    ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-DT'    ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-LS'    ,'FEB',None))
#
#  for i in range(10,23+1):
#    options = {'ACT':i}
#    matrixList.append(('DOWN'     ,'ALL' ,'ACT-BY-LOC','FEB',options))
#
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-WH'    ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-AWH'   ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-LT'    ,'FEB',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-OT'    ,'FEB',None))
#
#  summary.AddMatrixSheet('GLOBAL FEB',matrixList)
#
#  matrixList = []
#  matrixList.append(('START'    ,'ALL' ,'ACTIVITY'  ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'LTS'       ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-CF'    ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-PS'    ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-DT'    ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-LS'    ,'MAR',None))
#
#  for i in range(10,23+1):
#    options = {'ACT':i}
#    matrixList.append(('DOWN'     ,'ALL' ,'ACT-BY-LOC','MAR',options))
#
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-WH'    ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-AWH'   ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-LT'    ,'MAR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-OT'    ,'MAR',None))
#
#  summary.AddMatrixSheet('GLOBAL MAR',matrixList)
#
#  matrixList = []
#  matrixList.append(('START'    ,'ALL' ,'ACTIVITY'  ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'LTS'       ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-CF'    ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-PS'    ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-DT'    ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'UTL-LS'    ,'APR',None))
#
#  for i in range(10,23+1):
#    options = {'ACT':i}
#    matrixList.append(('DOWN'     ,'ALL' ,'ACT-BY-LOC','APR',options))
#
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-WH'    ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-AWH'   ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-LT'    ,'APR',None))
#  matrixList.append(('DOWN'     ,'ALL' ,'FAE-OT'    ,'APR',None))
#
#  summary.AddMatrixSheet('GLOBAL APR',matrixList)
#
#  summary.Order()
#  summary.Save('FAE GLOBAL MATRIX.xlsx')
#
  logging.debug('End of Program')
  
#  #emeaActList = [10,11,12,13,14,15,16,17,18,19,20,21,22,23]
#  #amActList   = emeaActList
#  #gcActList   = emeaActList
#  #emeaLocList = ['UK','Sweden','Finland','France','Germany','OTH']
#  #emeaOthList = ['Poland','Portugal','Spain','Ireland','Turkey']
#  #amLocList   = ['East','West','Canada','Latin America','South America']
#
#  matrixList = []
# 
#  options = {'ACT':10}
#  matrixList.append(('START'   ,'ALL','ACT-BY-LOC','ALL',options))
#  for i in range(10,23+1):
#    options = {'ACT':i}
#    matrixList.append(('DOWN','EMEA','ACT-BY-LOC','ALL',options))
#     
#  matrixList.append(('DOWN'    ,'EMEA','GKA'       ,'ALL',None))
#  matrixList.append(('DOWN'    ,'EMEA','OVERTIME'  ,'ALL',None))
#  matrixList.append(('DOWN'    ,'EMEA','UTL-DT'    ,'ALL',None))
#  matrixList.append(('DOWN'    ,'EMEA','UTL-LS'    ,'ALL',None))
#  matrixList.append(('DOWN'    ,'EMEA','UTL-PS'    ,'ALL',None))
#  matrixList.append(('DOWN'    ,'EMEA','UTL-CF'    ,'ALL',None))
#  matrixList.append(('DOWN'    ,'EMEA','LTS'       ,'ALL',None))
#  #matrixList.append(('DOWN',     'ALL',       'ACTIVITY', 'ALL'))
#  #matrixList.append(('DOWN',     'EMEA',      'ACTIVITY', 'APR'))
#  #matrixList.append(('DOWN',     'ALL',       'FAE-OT',   'ALL'))
#  #matrixList.append(('DOWN',     'ALL',       'FAE-LT',   'ALL'))
#  #matrixList.append(('DOWN',     'AM',        'FAE-AWH',  'ALL'))
#  #matrixList.append(('RIGHT',    'AM',        'FAE-WH',   'ALL'))
#  #matrixList.append(('DOWN-LEFT','EMEA',      'FAE-AWH',  'ALL'))
#  #matrixList.append(('RIGHT',    'EMEA',      'FAE-WH',   'ALL'))
#  #matrixList.append(('DOWN-LEFT','GC',        'FAE-AWH',  'ALL'))
#  #matrixList.append(('RIGHT',    'GC',        'FAE-WH',   'ALL'))
#  #matrixList.append(('DOWN',     ['AM','GC'], 'FAE-AWH',  'APR'))
#  #matrixList.append(('DOWN',     ['AM','GC'], 'FAE-AWH',  'FEB'))
###