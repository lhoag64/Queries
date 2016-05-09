import logging
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetUtlPsSum(db,region,weeks):

  c = db.cursor()

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT act.pre_sales,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_act AS act ON ts.activity = act.act
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY act.billable
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT act.pre_sales,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_act AS act ON ts.activity = act.act
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY act.billable
          ''',(region,wcDate,weDate))

    utlList = c.fetchall()

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT sum(ts.hours)
            FROM ts_entry AS ts
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT sum(ts.hours)
            FROM ts_entry AS ts
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
          ''',(region,wcDate,weDate))

    totList = c.fetchall()

    presale = 0.0
    for item in utlList:
      if (item[0] == 1):
        presale = item[1]
        break

    if (len(utlList) > 0):
      data = [presale,totList[0][0],presale/totList[0][0] * 100.0]
    else:
      data = [0.0,0.0,0.0]

    weekList.append(data)

  return weekList
