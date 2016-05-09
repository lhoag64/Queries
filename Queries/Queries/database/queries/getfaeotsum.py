import logging
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetFaeOtSum(db,region,weeks):

  c = db.cursor()

  if (region == 'ALL'):
    c.execute \
      ( \
        '''
          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
          FROM fae_team AS fae
          ORDER BY fae.lname,fae.fname
        ''')
  else:
    c.execute \
      ( \
        '''
          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
          FROM fae_team AS fae
          WHERE region = ?
          ORDER BY fae.lname,fae.fname
        ''',(region,))

  faes = c.fetchall()
  faeList = []
  faeDict = {}
  for fae in faes:
    faeList.append((fae[0],fae[1]))
    faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4])

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT ts.fname,ts.lname,wbs.leave,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY ts.fname,ts.lname,wbs.leave
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT ts.fname,ts.lname,wbs.leave,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            GROUP BY ts.fname,ts.lname,wbs.leave
          ''',(region,wcDate,weDate))

    hoursList = c.fetchall()
    resultSet = set([])
    wkHrsDict = {}
    for fae in hoursList:
      resultSet.add((fae[0],fae[1]))
      if ((fae[0],fae[1]) not in wkHrsDict):
        if (fae[2] == 0):
          wkHrsDict[(fae[0],fae[1])] = float(fae[3])
      else:
        if (fae[2] != 1):
          logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

    lvHrsDict = {}
    for fae in hoursList:
      if ((fae[0],fae[1]) not in lvHrsDict):
        if (fae[2] == 1):
          lvHrsDict[(fae[0],fae[1])] = float(fae[3])
      else:
        if (fae[2] != 0):
          logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

    data = []
    for fae in faeList:
      wkHours = 0.0
      lvHours = 0.0
      if ((fae[0],fae[1]) in wkHrsDict):
        wkHours = float(wkHrsDict[(fae[0],fae[1])])
      if ((fae[0],fae[1]) in lvHrsDict):
        lvHours = float(lvHrsDict[(fae[0],fae[1])])
      if ((fae[0],fae[1]) in resultSet):
        data.append((fae[0],fae[1],wkHours,lvHours))
      else:
        lvHrs = float(faeDict[(fae[0],fae[1])][0])
        data.append((fae[0],fae[1],0.0,lvHrs))

    weekList.append(data)

  return weekList
