import logging
import datetime
import sqlite3
from   xlinterface.xlworkbook  import XlWorkBook
from   xlinterface.xlworksheet import XlWorkSheet
from   database.tables.table   import Table

#----------------------------------------------------------------------
class WeeksTable(Table):
  def __init__(self):
    pass

  #--------------------------------------------------------------------
  def Create(self,db):
 
    c = db.cursor()

    try:
      c.execute('DROP TABLE weeks')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE weeks
             (
               week       TEXT,
               wc_date    TEXT,
               we_date    TEXT,
               am_days    TEXT,
               uk_days    TEXT,
               fr_days    TEXT,
               de_days    TEXT,
               fi_days    TEXT,
               se_days    TEXT,
               gc_days    TEXT,
               gc_week    TEXT
             )
        '''
      )

    db.commit()

    wb = XlWorkBook()
    wb.Read(r'X:\Reporting\Timesheets\Global-Working-Days-2016.xlsx')

    ws = wb.GetSheetByName('Weeks')

    index = 1
    weekList = []
    wsRow = 2
    wsCol = 1
    while (1):
      week = ws.GetValue(wsRow,wsCol+ 0)
      if (not week):
        break
      if (index == 1):
        wc_date = ws.GetValue(wsRow,wsCol+ 1)
        wc_date = str(wc_date)[:10]
        we_date = ws.GetValue(wsRow,wsCol+ 2)
        we_date = str(we_date)[:10]
      else:
        stxt    = wc_date.split('-')
        year    = int(stxt[0])
        mon     = int(stxt[1])
        day     = int(stxt[2])
        date    = datetime.date(year,mon,day)
        wc_date = date + datetime.timedelta(days= 7)
        we_date = date + datetime.timedelta(days=13)
        wc_date = wc_date.strftime('%Y-%m-%d')
        we_date = we_date.strftime('%Y-%m-%d')

      am_days   = ws.GetValue(wsRow,wsCol+ 3)
      uk_days   = ws.GetValue(wsRow,wsCol+ 4)
      fr_days   = ws.GetValue(wsRow,wsCol+ 5)
      de_days   = ws.GetValue(wsRow,wsCol+ 6)
      fi_days   = ws.GetValue(wsRow,wsCol+ 7)
      se_days   = ws.GetValue(wsRow,wsCol+ 8)
      gc_days   = ws.GetValue(wsRow,wsCol+ 9)
      gc_week   = ws.GetValue(wsRow,wsCol+10)

      week = (index,wc_date,we_date,am_days,uk_days,fr_days,de_days,fi_days,se_days,gc_days,gc_week)
      weekList.append(week)
      wsRow += 1
      index += 1

    c.executemany('INSERT INTO weeks VALUES (?,?,?,?,?,?,?,?,?,?,?)',weekList)

    db.commit()


  #--------------------------------------------------------------------
  def GetWeeks(self,db,period):

    weekTable =                                  \
      {                                          \
        'JAN'     : ('2016-01-04','2016-01-31'), \
        'FEB'     : ('2016-02-01','2016-02-28'), \
        'MAR'     : ('2016-02-29','2016-04-03'), \
        'APR'     : ('2016-04-04','2016-05-01'), \
        'MAY'     : ('2016-05-02','2016-05-29'), \
        'JUN'     : ('2016-05-30','2016-07-03'), \
        'JUL'     : ('2016-07-04','2016-05-32'), \
        'Q1FY2016': ('2016-01-04','2016-04-03'), \
        'H1FY2016': ('2016-01-04','2016-07-03')  \
      }
     
    c = db.cursor()
    c.execute('SELECT MAX(entry_date) FROM ts_entry')
    resultList = c.fetchall()

    now = datetime.date.today().strftime("%Y-%m-%d")
    max = resultList[0][0]

    weekStart = '2016-01-04'
    weekEnd   = max

    if (period != 'YTD'):
      if (period in weekTable):
        weekStart = weekTable[period][0]
        weekEnd   = weekTable[period][1]
        if (weekEnd > max):
          weekEnd = max
      else:
        logging.error('Invalid period:' + period)
        weekEnd = weekStart

    c.execute \
      ( \
        '''
           SELECT wc_date FROM weeks
           WHERE wc_date >= ? and wc_date <= ?
        '''
      ,(weekStart,weekEnd))

    resultList =  c.fetchall()
    return resultList
