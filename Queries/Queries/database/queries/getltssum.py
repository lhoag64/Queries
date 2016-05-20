#import logging
#import sqlite3
##from   database.queries.getwedate  import GetWeDate
##from   database.queries.regiondata import GetRegionWhereClause
#
##----------------------------------------------------------------------
#def GetLtsSum(db,regionList,weekDict,ltsList):
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
#    sqltxt  = 'SELECT fname,lname,region,work_type,wbs_code,entry_date'
#    sqltxt += '  FROM ts_entry AS ts'
#    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
#    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#    sqltxt += '  GROUP BY work_type,region,lname,fname'
#
#    c.execute(sqltxt,tuple(sqlopt))
#    detail = c.fetchall()
#
#    sqlopt  = [wcDate,weDate]
#    sqltxt  = 'SELECT work_type,SUM(hours)'
#    sqltxt += '  FROM ts_entry AS ts'
#    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
#    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#    sqltxt += '  GROUP BY work_type'
#
#    c.execute(sqltxt,tuple(sqlopt))
#    dbResult = c.fetchall()
#
#    resultDict = {'OTHER':0.0}
#    for result in dbResult:
#      if (result[0] and len(result[0]) > 0):
#        resultDict[result[0]] = result[1]
#      else:
#        resultDict['OTHER'] += float(result[1])
#
#    hours = []
#    if (ltsList):
#      for item in ltsList:
#        if (item[0] in resultDict):
#          tup = (item[0],float(resultDict[item[0]]))
#          hours.append(tup)
#        else:
#          tup = (item[0],0.0)
#          hours.append(tup)
#      tup = ('Other',float(resultDict['OTHER']))
#      hours.append(tup)
#    else:
#      throw
#
#    hoursList.append(hours)
#
#  if (dltWeekCnt != 0):
#    for i in range(dltWeekCnt):
#      hoursList.append(None)
#
#  return hoursList
#
##  weekList = []
##  for i in range(len(weeks)):
##
##    wcDate = weeks[i][0]
##    weDate = GetWeDate(wcDate)
##
##    if (region == 'ALL'):
##      c.execute \
##        ( \
##          '''
##            SELECT work_type, SUM(hours) AS total
##            FROM ts_entry AS ts
##            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
##            GROUP BY work_type
##          ''',(wcDate,weDate))
##    else:
##      c.execute \
##        ( \
##          '''
##            SELECT work_type, SUM(hours) AS total
##            FROM ts_entry AS ts
##            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
##            GROUP BY work_type
##          ''',(region,wcDate,weDate))
##
##    resultList = c.fetchall()
##    resultDict = {}
##    for result in resultList:
##      if (result[0] and len(result[0]) > 0):
##        resultDict[result[0]] = result[1]
##
##    data = []
##    for item in lts:
##      if (item[0] in resultDict):
##        data.append(float(resultDict[item[0]]))
##      else:
##        data.append(0.0)
##
##    weekList.append(data)
##
##  return weekList
#####