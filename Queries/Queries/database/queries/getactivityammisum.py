import logging
import sqlite3
#from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetActivityAmMiSum(db,region,act,weeks):

  c = db.cursor()

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT activity, SUM(hours) AS total
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and fae.prd_team = 'MI'
            GROUP BY activity
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT activity, SUM(hours) AS total
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and fae.prd_team = 'MI'
            GROUP BY activity
          ''',(region,wcDate,weDate))

    resultList = c.fetchall()
    resultDict = {}
    for result in resultList:
      if (result[0] and len(result[0]) > 0):
        resultDict[int(result[0])] = result[1]

    data = []
    for item in act:
      if (item[0] in resultDict):
        data.append(float(resultDict[item[0]]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList
