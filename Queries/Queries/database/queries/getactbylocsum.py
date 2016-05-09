import logging
import datetime
import re
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetActByLocSum(db,region,act,loc,weeks):

  locSet = set([])
  for item in loc:
    locSet.add(item)

  c = db.cursor()
  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT ts.activity,loc.loc,loc.desc,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_loc AS loc ON ts.work_loc = loc.loc
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
            GROUP BY ts.work_loc
          ''',(wcDate,weDate,act))
    else:
        c.execute \
        ( \
          '''
            SELECT ts.activity,loc.loc,loc.desc,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_loc AS loc ON ts.work_loc = loc.loc
            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
            GROUP BY ts.work_loc
          ''',(region,wcDate,weDate,act))

    resultList = c.fetchall()
    resultDict = {}
    resultDict['Other (EMEA)'] = 0
    for result in resultList:
      if (result[0] and len(result[0]) > 0):
        if (result[2] in locSet):
          resultDict[result[2]] = result[3]
        else:
          resultDict['Other (EMEA)'] += result[3]

    data = []
    for item in loc:
      if (item in resultDict):
        data.append(float(resultDict[item]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList

