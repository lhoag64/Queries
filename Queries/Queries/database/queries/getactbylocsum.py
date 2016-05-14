import logging
import sqlite3
from   database.queries.getwedate   import GetWeDate
from   database.queries.regiondata  import GetRegionWhereClause

KeyLocDict = { 'EMEA':'emea_key','AM':'am_key','GC':'gc_key'}

NameLookup =                         \
  {                                  \
    'US-EAST':'US-East',             \
    'US-WEST':'US-East',             \
    'CA'     :'CA-East',             \
    'UK'     :'UK',                  \
    'SE'     :'Sweden',              \
    'FI'     :'Finland',             \
    'FR'     :'France',              \
    'DE'     :'Germany',             \
    'GC-S'   :'Greater China South', \
    'GC-N'   :'Greater China North'  \
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
        if (key == 0 or name == 'GC'):
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

      if (region in ['AM','EMEA','APAC']):
        sqlopt  = [wcDate,weDate,act]
        sqltxt  = 'SELECT loc.loc_group,SUM(ts.hours)'
        sqltxt += '  FROM ts_entry AS ts'
        sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
        sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
        sqltxt += '  WHERE ts.region = \'' + region + '\''
        sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
        sqltxt += '    and ts.activity= ?'
        #sqltxt += '    and ' + KeyLocDict[region] + ' = 1'
        sqltxt += '  GROUP BY loc.loc_group'

        c.execute(sqltxt,tuple(sqlopt))
        dbResult = c.fetchall()

        hrsDict[region]['HOURS'].append(dbResult)

      else:
        sqlopt  = [wcDate,weDate,act]
        sqltxt  = 'SELECT fae.fae_loc,SUM(ts.hours)'
        sqltxt += '  FROM ts_entry AS ts'
        sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
        sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
        sqltxt += '  WHERE ts.region = \'' + region + '\''
        sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
        sqltxt += '    and ts.activity= ?'
        #sqltxt += '    and ' + KeyLocDict[region] + ' = 1'
        sqltxt += '  GROUP BY fae.fae_loc'

        c.execute(sqltxt,tuple(sqlopt))
        dbResult = c.fetchall()

        hrsList = []
        for item in dbResult:
          faeLoc = item[0]
          hrs    = item[1]
          for locTup in hrsDict[region]['LOCLIST']:
            loc = locTup[5][3:]
            if (loc == faeLoc):
              grp = locTup[2]
              hrsList.append((grp,hrs))

        if (len(hrsList) != 2):
          logging.warn('Hours list for GC expected to have 2 items')

        hrsDict[region]['HOURS'].append(hrsList)

  hoursDict = consolidate(regionList,minWeekCnt,hrsDict)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursDict['HRSLIST'].append(None)

  hoursDict['TITLE'] = title

  return hoursDict

#      sqlopt  = [wcDate,weDate,act]
#      sqltxt  = 'SELECT ts.fname,ts.lname,ts.work_loc,fae.fae_loc,loc.rgn_loc,ts.hours'
#      sqltxt += '  FROM ts_entry AS ts'
#      sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
#      sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
#      sqltxt += '  WHERE ts.region = \'' + region + '\''
#      sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#      sqltxt += '    and ts.activity= ?'
#      sqltxt += '    and ' + KeyLocDict[region] + ' = 1'
#      sqltxt += '  GROUP BY ts.work_loc,ts.fname,ts.lname'
#
#      c.execute(sqltxt,tuple(sqlopt))
#      keyDetail = c.fetchall()
#      c.execute(sqltxt,tuple(sqlopt))
#      keyResult = c.fetchall()
#      sqlopt  = [wcDate,weDate,act]
#      sqltxt  = 'SELECT ts.fname,ts.lname,ts.work_loc,fae.fae_loc,loc.rgn_loc,ts.hours'
#      sqltxt += '  FROM ts_entry AS ts'
#      sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
#      sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
#      sqltxt += '  WHERE ts.region = \'' + region + '\''
#      sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#      sqltxt += '    and ts.activity= ?'
#      sqltxt += '    and ' + KeyLocDict[region] + ' = 0'
#      sqltxt += '  GROUP BY ts.work_loc,ts.fname,ts.lname'
#
#      c.execute(sqltxt,tuple(sqlopt))
#      othDetail = c.fetchall()
#
#      sqlopt  = [wcDate,weDate,act]
#      sqltxt  = 'SELECT ts.work_loc,SUM(ts.hours)'
#      sqltxt += '  FROM ts_entry AS ts'
#      sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
#      sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
#      sqltxt += '  WHERE ts.region = \'' + region + '\''
#      sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#      sqltxt += '    and ts.activity= ?'
#      sqltxt += '    and ' + KeyLocDict[region] + ' = 0'
#      sqltxt += '  GROUP BY ts.work_loc'

#  locSet = set([])
#  for item in loc:
#    locSet.add(item)
#
#  c = db.cursor()
#  weekList = []
#  for i in range(len(weeks)):
#
#    wcDate = weeks[i][0]
#    weDate = GetWeDate(wcDate)
#
#    if (region == 'ALL'):
#      c.execute \
#        ( \
#          '''
#            SELECT ts.activity,loc.loc,loc.desc,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN ts_loc AS loc ON ts.work_loc = loc.loc
#            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
#            GROUP BY ts.work_loc
#          ''',(wcDate,weDate,act))
#    else:
#        c.execute \
#        ( \
#          '''
#            SELECT ts.activity,loc.loc,loc.desc,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN ts_loc AS loc ON ts.work_loc = loc.loc
#            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
#            GROUP BY ts.work_loc
#          ''',(region,wcDate,weDate,act))
#
#    resultList = c.fetchall()
#    resultDict = {}
#    resultDict['Other (EMEA)'] = 0
#    for result in resultList:
#      if (result[0] and len(result[0]) > 0):
#        if (result[2] in locSet):
#          resultDict[result[2]] = result[3]
#        else:
#          resultDict['Other (EMEA)'] += result[3]
#
#    data = []
#    for item in loc:
#      if (item in resultDict):
#        data.append(float(resultDict[item]))
#      else:
#        data.append(0.0)
#
#    weekList.append(data)
#
#  return weekList

