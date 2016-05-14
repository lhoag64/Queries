import logging
import sqlite3
from   database.queries.getwedate  import GetWeDate
from   database.queries.regiondata import GetRegionWhereClause

#----------------------------------------------------------------------
def GetUtlLsSum(db,regionList,weekDict):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    #sqlopt  = [wcDate,weDate]
    #sqltxt  = 'SELECT wbs.code,wbs.downtime,wbs.leave'
    #sqltxt += '  FROM ts_entry AS ts'
    #sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    #sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    #sqltxt += '    and wbs.leave = 1'
    #sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'

    #c.execute(sqltxt,tuple(sqlopt))
    #detail = c.fetchall()

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and wbs.leave = 1'
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'

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
      leave = utlResult[0][0]
      if (leave != None):
        tot   = totResult[0][0]
        tup   = [leave,tot,leave/tot * 100.0]
      else:
        tup = [0.0,0.0,0.0]
    else:
      tup = [0.0,0.0,0.0]

    hoursList.append(tup)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append(None)

  return hoursList



#
#    if (region == 'ALL'):
#      c.execute \
#        ( \
#          '''
#            SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
#            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.leave = 1)
#              GROUP BY wbs.code
#          ''',(wcDate,weDate))
#
#    utlList = c.fetchall()
#
#    if (len(utlList) > 0):
#      sum = 0.0
#      for item in utlList:
#        sum += item[3]
#      tot = totList[0][0]
#      data = [sum,tot,sum/tot * 100.0]
#    else:
#      data = [0.0,0.0,0.0]
#
#    weekList.append(data)
#
#  return weekList
