import logging
import datetime
import sqlite3
from   database.tables.table import Table

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
               wc_date TEXT
             )
        '''
      )

    year  = 2016
    weeks = []
    d = datetime.date(year,1,1)
    while (True):
      if (d.weekday() == 0):
        break;
      else:
        d = d + datetime.timedelta(days=1)
    i = 1
    while(True):
      weeks.append((d,))
      d = d + datetime.timedelta(days=7)
      if (d.year > year):
        break;
      i += 1

    c.executemany('INSERT INTO weeks VALUES (?)',weeks)

    db.commit()


  #--------------------------------------------------------------------
  def GetWeeks(self,db,period):

    weekTable =                             \
      {                                     \
        'JAN': ('2016-01-04','2016-01-31'), \
        'FEB': ('2016-02-01','2016-02-28'), \
        'MAR': ('2016-02-29','2016-04-03'), \
        'APR': ('2016-04-04','2016-04-24')  \
      }
     
    c = db.cursor()
    c.execute('SELECT MAX(entry_date) FROM ts_entry')
    resultList = c.fetchall()

    now = datetime.date.today().strftime("%Y-%m-%d")
    max = resultList[0][0]

    weekStart = '2016-01-04'
    weekEnd   = max

    if (period != 'ALL'):
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
