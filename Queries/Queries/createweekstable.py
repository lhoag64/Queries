import logging
import datetime
import sqlite3

#----------------------------------------------------------------------
def CreateWeeksTable(db):

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
 