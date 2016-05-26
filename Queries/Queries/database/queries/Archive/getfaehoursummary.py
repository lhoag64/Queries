import logging
import datetime
import re
import sqlite3

#----------------------------------------------------------------------
def GetFaeHourSummary(self,db,region,weeks):

  c = db.cursor()

  if (region == 'ALL'):
    c.execute \
      ( \
        '''
          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type,region
          FROM fae_team AS fae
          ORDER BY fae.region,fae.lname,fae.fname
        ''')
  else:
    c.execute \
      ( \
        '''
          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type,region
          FROM fae_team AS fae
          WHERE region = ?
          ORDER BY fae.region,fae.lname,fae.fname
        ''',(region,))

  faes = c.fetchall()
  faeList = []
  faeDict = {}
  for fae in faes:
    faeList.append((fae[0],fae[1]))
    faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4],fae[5])

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
            GROUP BY ts.fname,ts.lname
          ''',(wcDate,weDate))
    else:
      c.execute \
        ( \
          '''
            SELECT ts.fname,ts.lname,sum(ts.hours)
            FROM ts_entry AS ts
            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
            INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
            GROUP BY ts.fname,ts.lname
          ''',(region,wcDate,weDate))

    hoursList = c.fetchall()
    hoursDict = {}
    for fae in hoursList:
      if ((fae[0],fae[1]) not in hoursDict):
        hoursDict[(fae[0],fae[1])] = float(fae[2])
      else:
        logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

    data = []
    for fae in faeList:
      if ((fae[0],fae[1]) in hoursDict):
        actHours = float(hoursDict[(fae[0],fae[1])])
        data.append((fae[0],fae[1],actHours))
      else:
        data.append((fae[0],fae[1],0.0))

    weekList.append(data)

  faeAvgDict = {}
  for week in weekList:
    for fae in week:
      t = (fae[0],fae[1])
      if (t not in faeAvgDict):
        faeAvgDict[t] = {}
        faeAvgDict[t]['SUM'] = 0.0
        faeAvgDict[t]['CNT'] =   0
        faeAvgDict[t]['NRM'] = float(faeDict[t][0])
        faeAvgDict[t]['MAX'] = float(faeDict[t][1])
        faeAvgDict[t]['LBR'] = faeDict[t][2]
        faeAvgDict[t]['RGN'] = faeDict[t][3]
      faeAvgDict[t]['SUM'] += float(fae[2])
      faeAvgDict[t]['CNT'] += 1

  result = []
  for fae in faeList:
    t = (fae[0],fae[1])
    sum = faeAvgDict[t]['SUM']
    cnt = faeAvgDict[t]['CNT']
    nrm = faeAvgDict[t]['NRM']
    max = faeAvgDict[t]['MAX']
    lbr = faeAvgDict[t]['LBR']
    rgn = faeAvgDict[t]['RGN']
    avg = sum/float(cnt)
    ot  = avg - nrm
    name = fae[0] + ' ' + fae[1]
    result.append((name,avg,ot,nrm,max,lbr,rgn))

  return result

