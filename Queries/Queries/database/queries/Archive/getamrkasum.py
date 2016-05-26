import logging
import sqlite3
#from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetAmRkaSum(db,region,codes,weeks):

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
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and 
              (wbs.gl_tm_key_acct = 1 or wbs.am_tm_car_acct = 1 or 
               wbs.am_tm_smc_acct = 1 or wbs.am_mi_rka_acct = 1 or
               wbs.code = 'TTT' or wbs_code = 'COB' or wbs_code = 'OTH')
            GROUP BY wbs.code
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT wbs.code,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and 
              (wbs.gl_tm_key_acct = 1 or wbs.am_tm_car_acct = 1 or 
               wbs.am_tm_smc_acct = 1 or wbs.am_mi_rka_acct = 1 or
               wbs.code = 'TTT' or wbs_code = 'COB' or wbs_code = 'OTH')
            GROUP BY wbs.code
          ''',(region,wcDate,weDate))

    codesList = c.fetchall()
    codesDict = {}
    for code in codesList:
      if (code[0] and len(code[0]) > 0):
        if (code[0] == 'NSN'):
          if ('NOK' in codesDict):
            codesDict['NOK'] += code[1]
        else:
          codesDict[code[0]] = code[1]

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT wbs.code,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and 
              (wbs.gl_tm_key_acct = 0 and wbs.am_tm_car_acct = 0 and 
               wbs.am_tm_smc_acct = 0 and wbs.am_mi_key_acct = 0 and
               wbs.code <> 'TTT' and wbs_code <> 'COB' and wbs_code <> 'OTH')
            GROUP BY wbs.code
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT wbs.code,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
            WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and 
              (wbs.gl_tm_key_acct = 0 and wbs.am_tm_car_acct = 0 and 
               wbs.am_tm_smc_acct = 0 and wbs.am_mi_rka_acct = 0 and
               wbs.code <> 'TTT' and wbs_code <> 'COB' and wbs_code <> 'OTH')
            GROUP BY wbs.code
          ''',(region,wcDate,weDate))
    
    otherList = c.fetchall()
    otherSum = 0.0
    for item in otherList:
      code = item[0]
      hrs  = item[1]
      if (len(code) == 3):
        otherSum += hrs

    codesDict['OTHERS'] = otherSum

    data = []
    for item in codes:
      if (item in codesDict):
        data.append(float(codesDict[item]))
      else:
        data.append(0.0)

    weekList.append(data)

  return weekList
