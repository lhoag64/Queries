import logging
import sqlite3
from   database.queries.getwedate   import GetWeDate
from   database.queries.regiondata  import GetRegionWhereClause

KeyLocDict = { 'EMEA':'emea_key','AM':'am_key','GC':'gc_key'}

NameLookup =                         \
  {                                  \
    'US-EAST':'US-East',             \
    'US-WEST':'US-West',             \
    'CA'     :'CA-East',             \
    'UK'     :'UK',                  \
    'SE'     :'Sweden',              \
    'FI'     :'Finland',             \
    'FR'     :'France',              \
    'DE'     :'Germany',             \
    'GC'     :'Greater China'        \
  }

#----------------------------------------------------------------------
def consolidate(regionList,weekCnt,hrsDict):
  hoursDict = {}
  grpDict = {}
  for region in ['EMEA','GC','AM','APAC']:
    if (region in regionList):
      for idx in hrsDict[region]['LOCDICT']:
        locTup = hrsDict[region]['LOCDICT'][idx]
        key  = locTup[6]
        grp  = locTup[2]
        name = locTup[5]
        if (key == 0):
          name = 'Other (' + region + ')'
        else:
          name = NameLookup[name]
        grpDict[grp] = name
  grpList = sorted(grpDict.items())

  hoursDict['GRPDICT'] = grpDict
  hoursDict['GRPLIST'] = grpList
  hoursDict['HRSLIST'] = []

  weekList = []
  for i in range(weekCnt):
    hourData = {}
    for region in ['EMEA','GC','AM','APAC']:
      if (region in hrsDict):
        weekData = hrsDict[region]['HOURS']
        week = weekData[i]
        for item in week:
          hourData[item[0]] = item[1]

    hourList = []
    for item in hoursDict['GRPLIST']:
      if (item[0] in hourData):
        hourList.append((item[0],item[1],float(hourData[item[0]])))
      else:
        hourList.append((item[0],item[1],0.0))

    weekList.append(hourList)

  hoursDict['HRSLIST'] = weekList
  return hoursDict

#----------------------------------------------------------------------
def GetActByLocSum(db,regionList,weekDict,act):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hrsDict = {}

  sqlopt  = [act]
  sqltxt  = 'SELECT act,desc FROM ts_act WHERE act = ?'
  c.execute(sqltxt,tuple(sqlopt))
  actList = c.fetchall()
  title = actList[0][1] + ' - ' + str(actList[0][0])

  for region in regionList:
    if (region not in hrsDict):
      sqlopt  = []
      sqltxt  = 'SELECT loc,loc_order,loc_group,desc,rgn_desc,rgn_loc,' + KeyLocDict[region]
      sqltxt += '  FROM ts_loc'
      sqltxt += '  WHERE region = \'' + region + '\''
      sqltxt += '  ORDER BY loc_group,loc_order'

      c.execute(sqltxt,tuple(sqlopt))
      locList = c.fetchall()

      grpDict = {}
      for item in locList:
        grpDict[item[2]] = item

      hrsDict[region] = {'HOURS':[],'LOCLIST':locList,'LOCDICT':grpDict}

  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    for region in regionList:

      sqlopt  = [wcDate,weDate,act]
      sqltxt  = 'SELECT loc.loc_group,SUM(ts.hours)'
      sqltxt += '  FROM ts_entry AS ts'
      sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
      sqltxt += '  WHERE ts.region = \'' + region + '\''
      sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
      sqltxt += '    and ts.activity= ?'
      #sqltxt += '    and ' + KeyLocDict[region] + ' = 1'
      sqltxt += '  GROUP BY loc.loc_group'

      c.execute(sqltxt,tuple(sqlopt))
      dbResult = c.fetchall()

      hrsDict[region]['HOURS'].append(dbResult)

  hoursDict = consolidate(regionList,minWeekCnt,hrsDict)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursDict['HRSLIST'].append(None)

  hoursDict['TITLE'] = title

  return hoursDict

