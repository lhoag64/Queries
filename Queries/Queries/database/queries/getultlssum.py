import logging
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetUtlLsSum(db,region,weeks):

  c = db.cursor()

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.leave = 1)
              GROUP BY wbs.code
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.leave = 1)
            GROUP BY wbs.code
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

    if (len(utlList) > 0):
      sum = 0.0
      for item in utlList:
        sum += item[3]
      tot = totList[0][0]
      data = [sum,tot,sum/tot * 100.0]
    else:
      data = [0.0,0.0,0.0]

    weekList.append(data)

  return weekList
