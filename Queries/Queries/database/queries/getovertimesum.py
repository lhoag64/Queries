import logging
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetOverTimeSum(db,region,weeks):

  c = db.cursor()
  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT sum(norm_hours) FROM fae_team
          ''')
    else:
      c.execute \
        ( \
          '''
          SELECT sum(norm_hours) FROM fae_team WHERE region = ?
          ''',(region,))

    nrmList = c.fetchall()

    if (region == 'ALL'):
      c.execute \
      ( \
          '''
            SELECT sum(hours)
            FROM ts_entry AS ts
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
          ''',(wcDate,weDate))
    else:
      c.execute \
      ( \
          '''
            SELECT sum(hours)
            FROM ts_entry AS ts
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
          ''',(region,wcDate,weDate))

    totList = c.fetchall()

    if (totList[0][0]):
      nrm = nrmList[0][0]
      tot = totList[0][0]
      ot  = tot - nrm
      data = [ot,nrm,ot/tot * 100.0]
    else:
      data = [0.0,0.0,0.0]
    #logging.debug(str(data[0]).rjust(5) + ' ' + str(data[1]).rjust(5))

    weekList.append(data)

  return weekList
