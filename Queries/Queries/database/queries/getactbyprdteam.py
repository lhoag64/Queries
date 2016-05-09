import logging
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetActByPrdTeam(db,region,act,prdList,weeks):

  prdSet = set([])
  for item in prdList:
    prdSet.add(item)

  c = db.cursor()
  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT ts.activity,fae.prd_team,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
            GROUP BY ts.activity,fae.prd_team
          ''',(wcDate,weDate,act))
    else:
      c.execute \
        ( \
          '''
            SELECT ts.activity,fae.prd_team,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            WHERE fae.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
            GROUP BY ts.activity,fae.prd_team
          ''',(region,wcDate,weDate,act))

    resultList = c.fetchall()
    resultDict = {}
    for result in resultList:
      if (len(result) == 3):
        if (result[1] in prdSet):
          resultDict[result[1]] = result[2]

    data = []
    for item in prdList:
      if (item in resultDict):
        data.append(float(resultDict[item]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList


