import logging
import sqlite3
#from   database.queries.getwedate import GetWeDate
#from   database.queries.regiondata  import GetRegionWhereClause

#----------------------------------------------------------------------
def GetFaeLtSum(db,regionList,weekDict):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    #----------------------------------------------------------------
    sqlopt  = [wcDate,weDate,wcDate,weDate]
    sqltxt  = 'SELECT fae.lbr_type,sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
    sqltxt += '  INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'
    sqltxt += '  GROUP BY fae.lbr_type'

    c.execute(sqltxt,tuple(sqlopt))
    dbResult = c.fetchall()

    hoursDict = {}
    for item in dbResult:
      if (item[0] not in hoursDict):
        hoursDict[item[0]] = item[1]

    data = []
    for item in ['P','C']:
      if (item in hoursDict):
        data.append(float(hoursDict[item]))
      else:
        data.append(0.0)

    hoursList.append(data)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append([None,None])

  return hoursList


#  c = db.cursor()
#
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
#            SELECT fae.lbr_type,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
#            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
#            GROUP BY fae.lbr_type
#          ''',(wcDate,weDate))
#    else:
#      c.execute \
#          ( \
#          '''
#            SELECT fae.lbr_type,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
#            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
#            GROUP BY fae.lbr_type
#          ''',(region,wcDate,weDate))
#
#    hoursList = c.fetchall()
#    hoursDict = {}
#    for item in hoursList:
#      if (item[0] not in hoursDict):
#        hoursDict[item[0]] = item[1]
#
#    data = []
#    for item in ['P','C']:
#      if (item in hoursDict):
#        data.append(float(hoursDict[item]))
#      else:
#        data.append(0.0)
#
#    weekList.append(data)
#
#  return weekList
