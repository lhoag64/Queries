#import logging
#import sqlite3
#from   database.queries.getwedate  import GetWeDate
#from   database.queries.regiondata import GetRegionWhereClause
#
##----------------------------------------------------------------------
#def GetUtlCfSum(db,regionList,weekDict):
#
#  c = db.cursor()
#
#  minWeekCnt = len(weekDict['MIN'])
#  maxWeekCnt = len(weekDict['MAX'])
#  dltWeekCnt = maxWeekCnt - minWeekCnt
#
#  hoursList = []
#  for i in range(minWeekCnt):
#
#    wcDate = weekDict['MIN'][i][0]
#    weDate = GetWeDate(wcDate)
#
#    sqlopt  = [wcDate,weDate]
#    sqltxt  = 'SELECT sum(ts.hours)'
#    sqltxt += '  FROM ts_entry AS ts'
#    sqltxt += '  INNER JOIN ts_act AS act ON ts.activity = act.act'
#    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
#    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#    sqltxt += '    and act.billable = 1'
#
#    c.execute(sqltxt,tuple(sqlopt))
#    utlResult = c.fetchall()
#
#    sqlopt  = [wcDate,weDate]
#    sqltxt  = 'SELECT sum(ts.hours)'
#    sqltxt += '  FROM ts_entry AS ts'
#    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
#    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#
#    c.execute(sqltxt,tuple(sqlopt))
#    totResult = c.fetchall()
#
#    if (len(utlResult) > 0):
#      billable = utlResult[0][0]
#      tot      = totResult[0][0]
#      tup = [billable,tot,billable/tot * 100.0]
#    else:
#      tup = [0.0,0.0,0.0]
#
#    hoursList.append(tup)
#
#  if (dltWeekCnt != 0):
#    for i in range(dltWeekCnt):
#      hoursList.append(None)
#
#  return hoursList
#######
