import logging
import sqlite3
from   database.queries.getwedate  import GetWeDate
from   database.queries.regiondata import GetRegionWhereClause

#----------------------------------------------------------------------
def GetGkaSum(db,regionList,weekDict,codeList):
  c = db.cursor()

  minWeekCnt = len(weekDict['MIN'])
  maxWeekCnt = len(weekDict['MAX'])
  dltWeekCnt = maxWeekCnt - minWeekCnt

  hoursList = []
  for i in range(minWeekCnt):

    wcDate = weekDict['MIN'][i][0]
    weDate = GetWeDate(wcDate)

#            SELECT wbs.code,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
#            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and 
#              (wbs.gl_tm_key_acct = 1 or wbs.code = 'TTT' or wbs_code = 'COB' or wbs_code = 'OTH')
#            GROUP BY wbs.code
#          ''',(region,wcDate,weDate))

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT wbs.code,SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and (wbs.gl_tm_key_acct = 1 or'
    sqltxt += '         wbs.code = \'TTT\' or  wbs.code = \'COB\' or wbs.code = \'OTH\')'
    sqltxt += '  GROUP BY wbs.code'

    c.execute(sqltxt,tuple(sqlopt))
    gkaResult = c.fetchall()

    codeDict = {}
    for code in gkaResult:
      if (code[0] and len(code[0]) > 0):
        if (code[0] == 'NSN'):
          if ('NOK' in codeDict):
            codeDict['NOK'] += code[1]
        else:
          codeDict[code[0]] = code[1]

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT wbs.code,SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + GetRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and (wbs.gl_tm_key_acct = 0 and'
    sqltxt += '         wbs.code <> \'TTT\' and  wbs.code <> \'COB\' and wbs.code <> \'OTH\')'
    sqltxt += '  GROUP BY wbs.code'

    c.execute(sqltxt,tuple(sqlopt))
    othResult = c.fetchall()

    othSum = 0.0
    for item in othResult:
      code = item[0]
      hrs  = item[1]
      if (len(code) == 3):
        othSum += hrs
    codeDict['OTHERS'] = othSum

    hours = []
    for item in codeList:
      if (item in codeDict):
        hours.append((item,float(codeDict[item])))
      else:
        hours.append((item,0.0))

    hoursList.append(hours)

  if (dltWeekCnt != 0):
    for i in range(dltWeekCnt):
      hoursList.append(None)

  return hoursList

#    otherList = c.fetchall()
#    otherSum = 0.0
#    for item in otherList:
#      code = item[0]
#      hrs  = item[1]
#      if (len(code) == 3):
#        otherSum += hrs
#
#    codesDict['OTHERS'] = otherSum
#
#    data = []
#    for item in codes:
#      if (item in codesDict):
#        data.append(float(codesDict[item]))
#      else:
#        data.append(0.0)
#
#    weekList.append(data)
#
#  return weekList
###