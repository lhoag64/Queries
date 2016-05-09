import logging
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetLtsSum(db,region,lts,weeks):

  c = db.cursor()

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT work_type, SUM(hours) AS total
            FROM ts_entry AS ts
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY work_type
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT work_type, SUM(hours) AS total
            FROM ts_entry AS ts
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY work_type
          ''',(region,wcDate,weDate))

    resultList = c.fetchall()
    resultDict = {}
    for result in resultList:
      if (result[0] and len(result[0]) > 0):
        resultDict[result[0]] = result[1]

    data = []
    for item in lts:
      if (item[0] in resultDict):
        data.append(float(resultDict[item[0]]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList
