import logging
import sqlite3
from   database.queries.getwedate  import GetWeDate
from   database.queries.regiondata import GetRegionWhereClause

#----------------------------------------------------------------------
def GetUtlCfSum(db,regionList,weekDict):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_act AS act ON ts.activity = act.act'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and act.billable = 1'

    c.execute(sqltxt,tuple(sqlopt))
    utlResult = c.fetchall()

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'

    c.execute(sqltxt,tuple(sqlopt))
    totResult = c.fetchall()

    if (len(utlResult) > 0):
      billable = utlResult[0][0]
      tot      = totResult[0][0]
      tup = [billable,tot,billable/tot * 100.0]
    else:
      tup = [0.0,0.0,0.0]

    hoursList.append(tup)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append(None)

  return hoursList

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
#            SELECT act.billable,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN ts_act AS act ON ts.activity = act.act
#            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
#            GROUP BY act.billable
#          ''',(wcDate,weDate))
#    else:
#      c.execute \
#        ( \
#          '''
#            SELECT act.billable,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN ts_act AS act ON ts.activity = act.act
#            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
#            GROUP BY act.billable
#          ''',(region,wcDate,weDate))
#
#    utlList = c.fetchall()
#
#    if (region == 'ALL'):
#      c.execute \
#        ( \
#          '''
#            SELECT sum(ts.hours)
#            FROM ts_entry AS ts
#            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
#          ''',(wcDate,weDate))
#    else:
#      c.execute \
#        ( \
#          '''
#            SELECT sum(ts.hours)
#            FROM ts_entry AS ts
#            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
#          ''',(region,wcDate,weDate))
#
#    totList = c.fetchall()
#
#    billable = 0.0
#    for item in utlList:
#      if (item[0] == 1):
#        billable = item[1]
#        break
#
#    if (len(utlList) > 0):
#      data = [billable,totList[0][0],billable/totList[0][0] * 100.0]
#    else:
#      data = [0.0,0.0,0.0]
#
#    weekList.append(data)
#
#  return weekList
