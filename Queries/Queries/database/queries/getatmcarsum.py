import logging
import sqlite3
#from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetAmTmCarSum(db,region,codes,weeks):

  c = db.cursor()
  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT wbs.code,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.am_tm_car_acct = 1)
            GROUP BY wbs.code
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT wbs.code,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.am_tm_car_acct = 1)
            GROUP BY wbs.code
          ''',(region,wcDate,weDate))

    codesList = c.fetchall()
    codesDict = {}
    for code in codesList:
        if (code[0] and len(code[0]) > 0):
          codesDict[code[0]] = code[1]

    data = []
    for item in codes:
      if (item in codesDict):
        data.append(float(codesDict[item]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList
