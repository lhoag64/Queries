import logging
import sqlite3
from   database.queries.getwedate  import GetWeDate
from   database.queries.regiondata import GetRegionWhereClause

#----------------------------------------------------------------------
def GetOverTimeSum(db,regionList,weekDict):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    #sqlopt  = [wcDate,weDate]
    #sqltxt  = 'SELECT fae.fname,fae.lname,fae.start_date,fae.end_date'
    #sqltxt += '  FROM fae_team AS fae'
    #sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'fae.region')
    #sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'
    #sqltxt += '  ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'

    #c.execute(sqltxt,tuple(sqlopt))
    #hc = c.fetchall()

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT SUM(fae.norm_hours)'
    sqltxt += '  FROM fae_team AS fae'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'fae.region')
    sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'

    c.execute(sqltxt,tuple(sqlopt))
    nrmResult = c.fetchall()

    #sqlopt  = []
    #sqltxt  = 'SELECT SUM(fae.norm_hours)'
    #sqltxt += '  FROM fae_team AS fae'
    #sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'fae.region')

    #c.execute(sqltxt,tuple(sqlopt))
    #nrmResult = c.fetchall()

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'

    c.execute(sqltxt,tuple(sqlopt))
    totResult = c.fetchall()

    nrm = nrmResult[0][0]
    tot = totResult[0][0]
    if (nrm != None and tot != None):
      ot = tot - nrm
      if (ot < 0.0):
        ot = 0.0
      tup = [ot,nrm,ot/nrm * 100.0]
    else:
      tup = [0.0,0.0,0.0]

    hoursList.append(tup)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append(None)

  return hoursList

#    SELECT sum(norm_hours) FROM fae_team
#    nrmList = c.fetchall()
#
#    SELECT sum(hours)
#    FROM ts_entry AS ts
#    WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
#    totList = c.fetchall()
#
#    if (totList[0][0]):
#      nrm = nrmList[0][0]
#      tot = totList[0][0]
#      ot  = tot - nrm
#      data = [ot,nrm,ot/tot * 100.0]
#    else:
#      data = [0.0,0.0,0.0]
#    #logging.debug(str(data[0]).rjust(5) + ' ' + str(data[1]).rjust(5))
#
#    weekList.append(data)
#
#  return weekList
