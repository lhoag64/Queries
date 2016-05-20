import logging
import sqlite3
#from   database.queries.getwedate   import GetWeDate
from   database.queries.faedata     import FaeData
from   database.queries.faedata     import FaeHoursData
from   database.queries.faedata     import FaeSumData
from   database.queries.faedata     import FaeWorkingDays
#from   database.queries.regiondata  import GetRegionWhereClause

#----------------------------------------------------------------------
def GetFaeOtSum(db,regionList,weekDict):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

 #------------------------------------------------------------------
  sqlopt = []
  sqltxt  = 'SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type,start_date,end_date,region'
  sqltxt += '  FROM fae_team AS fae'
  sqltxt += '  WHERE ' + GetRegionWhereClause(regionList)
  sqltxt += '  ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'

  c.execute(sqltxt,tuple(sqlopt))
  faes = c.fetchall()
  #------------------------------------------------------------------

  faeList = []
  faeDict = {}
  for fae in faes:
    faeData = FaeData(fae[0],fae[1],fae[2],fae[3],fae[4],fae[5],fae[6],fae[7])
    faeList.append(faeData)
    faeDict[(fae[0],fae[1])] = faeData

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    #----------------------------------------------------------------

    sqlopt  = [wcDate]
    sqltxt  = 'SELECT week,am_days,uk_days,fr_days,de_days,fi_days,se_days,gc_days'
    sqltxt += '  FROM weeks'
    sqltxt += '  WHERE wc_date == ?'

    c.execute(sqltxt,tuple(sqlopt))
    weekData = c.fetchall()

    workingDays = FaeWorkingDays()
    workingDays.weekNum = int(weekData[0][0])
    workingDays.am_days = int(weekData[0][1])
    workingDays.uk_days = int(weekData[0][2])
    workingDays.fr_days = int(weekData[0][3])
    workingDays.de_days = int(weekData[0][4])
    workingDays.fi_days = int(weekData[0][5])
    workingDays.se_days = int(weekData[0][6])
    workingDays.gc_days = int(weekData[0][7])

    #----------------------------------------------------------------

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT fae.fname,fae.lname,fae.start_date,fae.end_date'
    sqltxt += '  FROM fae_team AS fae'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'fae.region')
    sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'
    sqltxt += '  ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'

    c.execute(sqltxt,tuple(sqlopt))
    hc = c.fetchall()

    #----------------------------------------------------------------

    hc = len(hc)

    #----------------------------------------------------------------

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT ts.fname,ts.lname,sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
    sqltxt += '  INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0'
    sqltxt += '  GROUP BY ts.fname,ts.lname'

    c.execute(sqltxt,tuple(sqlopt))
    wkList = c.fetchall()

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT ts.fname,ts.lname,sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
    sqltxt += '  INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 1'
    sqltxt += '  GROUP BY ts.fname,ts.lname'

    c.execute(sqltxt,tuple(sqlopt))
    lvList = c.fetchall()

    #----------------------------------------------------------------

    wkHrsDict = {}
    for tup in wkList:
      name = (tup[0],tup[1])
      if (name not in wkHrsDict):
        wkHrsDict[name] = float(tup[2])
      else:
        logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

    lvHrsDict = {}
    for tup in lvList:
      name = (tup[0],tup[1])
      if (name not in lvHrsDict):
        lvHrsDict[name] = float(tup[2])
      else:
        logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

    hours = []
    for faeData in faeList:
      fname   = faeData.fname
      lname   = faeData.lname
      name    = (fname,lname)
      sDate   = faeData.startDate
      eDate   = faeData.endDate
      wkHours = 0.0
      lvHours = 0.0
      nrHours = float(faeDict[name].nrmHrs)
      if (wcDate >= sDate and weDate <= eDate):
        if (name in wkHrsDict):
          wkHours = float(wkHrsDict[name])
        if (name in lvHrsDict):
          lvHours = float(lvHrsDict[name])
        hours.append((fname,lname,wkHours,lvHours,nrHours))
      else:
        hours.append((fname,lname,None,None,None))
    
    hoursList.append(FaeHoursData(workingDays,hc,hours))

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append(FaeHoursData(None,None,None))

  return FaeSumData(faeList,hoursList)
