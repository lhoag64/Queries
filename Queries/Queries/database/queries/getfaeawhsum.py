import logging
import datetime
import sqlite3
from   database.queries.getwedate import GetWeDate

#----------------------------------------------------------------------
def GetFaeAwhSum(db,region,weeks):

  c = db.cursor()

 #------------------------------------------------------------------
  sqlopt    = [region]
  sqltxt    = [''] * 10
  sqltxt[0] = 'SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type'
  sqltxt[1] = 'FROM fae_team AS fae'
  sqltxt[2] = 'WHERE region = ?'
  sqltxt[3] = 'ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'
  if (region == 'ALL'):
    sqltxt.pop(2)
    sqlopt.pop(0)

  sqltxt = ' '.join(sqltxt)
  sqlopt = tuple(sqlopt)

  c.execute(sqltxt,sqlopt)
  faes = c.fetchall()
  #------------------------------------------------------------------

  faeList = []
  faeDict = {}
  for fae in faes:
    faeList.append((fae[0],fae[1]))
    faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4])

  weekList = []
  for i in range(len(weeks)):

    wcDate = weeks[i][0]
    weDate = GetWeDate(wcDate)

    #----------------------------------------------------------------
    sqlopt    = [wcDate]
    sqltxt    = [''] * 10
    sqltxt[0] = 'SELECT week,am_days,uk_days,fr_days,de_days,fi_days,se_days,gc_days'
    sqltxt[1] = 'FROM weeks'
    sqltxt[2] = 'WHERE wc_date == ?'

    sqltxt = ' '.join(sqltxt)
    sqlopt = tuple(sqlopt)

    c.execute(sqltxt,sqlopt)
    weekData = c.fetchall()

    weekNum = weekData[0][0]
    am_days = weekData[0][1]
    uk_days = weekData[0][2]
    fr_days = weekData[0][3]
    de_days = weekData[0][4]
    fi_days = weekData[0][5]
    se_days = weekData[0][6]
    gc_days = weekData[0][7]

    #----------------------------------------------------------------
    sqlopt    = [region,wcDate,weDate]
    sqltxt    = [''] * 10
    sqltxt[0] = 'SELECT fae.fname,fae.lname,fae.start_date,fae.end_date'
    sqltxt[1] = 'FROM fae_team AS fae'
    sqltxt[2] = 'WHERE'
    sqltxt[3] = '  region = ? and'
    sqltxt[4] = '  fae.start_date <= ? and fae.end_date >= ?'
    sqltxt[5] = 'ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'
    if (region == 'ALL'):
      sqltxt.pop(3)
      sqlopt.pop(0)

    sqltxt = ' '.join(sqltxt)
    sqlopt = tuple(sqlopt)

    c.execute(sqltxt,sqlopt)
    hc = c.fetchall()
    #----------------------------------------------------------------

    hc = len(hc)
    logging.debug('HC ' + str(hc) + ' ' + wcDate + ' ' + weDate)

    #----------------------------------------------------------------
    sqlopt    = [region,wcDate,weDate]
    sqltxt    = [''] * 10
    sqltxt[0] = 'SELECT ts.fname,ts.lname,sum(ts.hours)'
    sqltxt[1] = 'FROM ts_entry AS ts'
    sqltxt[2] = 'INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
    sqltxt[3] = 'INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)'
    sqltxt[4] = 'WHERE'
    sqltxt[5] = '  ts.region = ? and'
    sqltxt[6] = '  (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0'
    sqltxt[7] = 'GROUP BY ts.fname,ts.lname'
    if (region == 'ALL'):
      sqltxt.pop(5)
      sqlopt.pop(0)

    sqltxt = ' '.join(sqltxt)
    sqlopt = tuple(sqlopt)

    c.execute(sqltxt,sqlopt)
    hoursList = c.fetchall()
    #----------------------------------------------------------------

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

  return weekList


#def GetFaeAwhSum(db,region,weeks):
#
#  c = db.cursor()
#
#  if (region == 'ALL'):
#    c.execute \
#      ( \
#        '''
#          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
#          FROM fae_team AS fae
#          ORDER BY fae.lname,fae.fname
#        ''')
#  else:
#    c.execute \
#      ( \
#        '''
#          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
#          FROM fae_team AS fae
#          WHERE region = ?
#          ORDER BY fae.lname,fae.fname
#        ''',(region,))
#
#  faes = c.fetchall()
#  faeList = []
#  faeDict = {}
#  for fae in faes:
#    faeList.append((fae[0],fae[1]))
#    faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4])
#
#  weekList = []
#  for i in range(len(weeks)):
#
#    wcDate = weeks[i][0]
#    weDate = GetWeDate(wcDate)
#
#    if (region == 'ALL'):
#      c.execute \
#        ( \
#          '''
#            SELECT ts.fname,ts.lname,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
#            INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
#            WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
#            GROUP BY ts.fname,ts.lname
#          ''',(wcDate,weDate))
#    else:
#      c.execute \
#        ( \
#          '''
#            SELECT ts.fname,ts.lname,sum(ts.hours)
#            FROM ts_entry AS ts
#            INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
#            INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
#            WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
#            GROUP BY ts.fname,ts.lname
#          ''',(region,wcDate,weDate))
#
#    hoursList = c.fetchall()
#    hoursDict = {}
#    for fae in hoursList:
#      if ((fae[0],fae[1]) not in hoursDict):
#        hoursDict[(fae[0],fae[1])] = float(fae[2])
#      else:
#        logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])
#
#    data = []
#    for fae in faeList:
#      if ((fae[0],fae[1]) in hoursDict):
#        actHours = float(hoursDict[(fae[0],fae[1])])
#        data.append((fae[0],fae[1],actHours))
#      else:
#        data.append((fae[0],fae[1],0.0))
#
#    weekList.append(data)
#
#  return weekList
###