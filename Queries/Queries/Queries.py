import logging
import os
from   utilities.logconfig         import LogConfig
from   utilities.args              import ParseArgs
from   utilities.readconfig        import ReadConfig
from   database                    import Database as Db
from   timesheet.calendar          import Calendar
from   timesheet.faeteam           import FaeTeam
from   timesheet.fldata            import FlData
from   timesheet.tsdata            import TsData
from   summary.wbdata              import WbData

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
def CreateWsList(wkSheets):

  #--------------------------------------------------------------------
  wsList = []
  for wkSheet in wkSheets:
    name = wkSheets[wkSheet]['NAME']
    objects = wkSheets[wkSheet]['OBJS']
    for object in objects:
      obj = objects[object]
      tup = (obj[0],obj[7],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6],object,name)
      wsList.append(tup)

  return wsList

#----------------------------------------------------------------------
if (__name__ == '__main__'):

  args    = ParseArgs()
  cfgDict = ReadConfig(args['CONFIG'])

  os.chdir(cfgDict['WORKDIR'])

  LogConfig('queries.log')
  logging.debug('Start of Program')

  Db(cfgDict['WORKDIR'],cfgDict['DATABASE'])

  if (True):
    InitializeDatabaseTables()
    InitializeTimesheetTables()

  for wkBook in cfgDict['WKBOOKS']:
    wbFilename = cfgDict['WKBOOKS'][wkBook]['FILENAME']
    wkSheets   = cfgDict['WKBOOKS'][wkBook]['WKSHEETS'] 
    wsList     = CreateWsList(wkSheets)

    wbData = WbData()

    wbData.AddList(wsList)
    wbData.Process()

    wbData.Order()
    wbData.Save(wbFilename)

  logging.debug('End of Program')

#  amList =                                                                                          \
#    [                                                                                               \
#      ((' 0',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACTIVITY'     ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','LTS'          ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','UTL-CF'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','UTL-PS'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','UTL-DT'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','UTL-LS'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','UTL-OT'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','GKA'          ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'10',{'ACT':10})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'11',{'ACT':11})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'12',{'ACT':12})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'13',{'ACT':13})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'14',{'ACT':14})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'15',{'ACT':15})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'16',{'ACT':16})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'17',{'ACT':17})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'18',{'ACT':18})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'19',{'ACT':19})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'20',{'ACT':20})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'21',{'ACT':21})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'22',{'ACT':22})  ,  \
#      (('+1',' 0'),'MATRIX EMEA YTD'    ,'MATRIX' ,'EMEA','YTD','ACT-BY-LOC'   ,'23',{'ACT':23})  ,  \
#      ((' 0',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','YTD','FAE-AWH'      ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','YTD','FAE-WH'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','YTD','FAE-OT'       ,None,None)        ,  \
#      (('+1',' 0'),'MATRIX EMEA FAE YTD','MATRIX' ,'EMEA','YTD','LTYPE'        ,None,None)        ,  \
#      ((' 0',' 0'),'SUMMARY EMEA YTD'   ,'SUMMARY','EMEA','YTD','STD'          ,None,None)         \
#    ]                                                                                     \
  