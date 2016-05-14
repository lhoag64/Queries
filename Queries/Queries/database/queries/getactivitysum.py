import logging
import sqlite3
from   database.queries.getwedate  import GetWeDate
from   database.queries.regiondata import GetRegionWhereClause

#----------------------------------------------------------------------
def GetActivitySum(db,regionList,weekDict,actList=None):

  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT fname,lname,region,activity,wbs_code,entry_date'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '  GROUP BY activity,region,lname,fname'

    c.execute(sqltxt,tuple(sqlopt))
    detail = c.fetchall()

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT activity,SUM(hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '  GROUP BY activity'

    c.execute(sqltxt,tuple(sqlopt))
    dbResult = c.fetchall()

    resultDict = {'OTHER':0.0}
    for result in dbResult:
      if (result[0] and len(result[0]) > 0):
        resultDict[int(result[0])] = result[1]
      else:
        resultDict['OTHER'] += float(result[1])

    hours = []
    if (actList):
      for item in actList:
        if (item[0] in resultDict):
          tup = (item[0],item[1],float(resultDict[item[0]]))
          hours.append(tup)
        else:
          tup = (item[0],item[1],0.0)
          hours.append(tup)
      tup = ('OTHER','Other',float(resultDict['OTHER']))
      hours.append(tup)
    else:
      throw

    hoursList.append(hours)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append(None)

  return hoursList
