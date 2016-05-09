import logging
import datetime
import sqlite3

#----------------------------------------------------------------------
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
