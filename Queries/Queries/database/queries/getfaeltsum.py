import logging
import datetime
import re
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
def GetFaeLtSum(self,db,region,weeks):

  c = db.cursor()

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT fae.lbr_type,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY fae.lbr_type
          ''',(wcDate,weDate))
    else:
      c.execute \
          ( \
          '''
            SELECT fae.lbr_type,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY fae.lbr_type
          ''',(region,wcDate,weDate))

    hoursList = c.fetchall()
    hoursDict = {}
    for item in hoursList:
      if (item[0] not in hoursDict):
        hoursDict[item[0]] = item[1]

    data = []
    for item in ['P','C']:
      if (item in hoursDict):
        data.append(float(hoursDict[item]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList
