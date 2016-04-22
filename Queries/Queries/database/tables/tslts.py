import logging
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsLtsTable(Table):
  def __init__(self):
    pass

  def Create(self,db):

    c = db.cursor()

    lts = [('Labour',),('Travel',),('Stand-By',)]

    try:
      c.execute('DROP TABLE ts_lts')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_lts
             (
               key         TEXT UNIQUE PRIMARY KEY
             )
        '''
      )

    c.executemany('INSERT INTO ts_lts VALUES (?)',lts)
    db.commit()

  #--------------------------------------------------------------------
  def GetLts(self,db,type):

    c = db.cursor()

    if (type == 'ALL'):
      pass

    c.execute(' SELECT key FROM ts_lts')

    ltslist = c.fetchall()

    return ltslist

#'''
#      c = db.cursor()
#
#  c.execute('SELECT wc_date FROM weeks ORDER BY wc_date')
#
#  week = []
#  for row in c.fetchall():
#    week.append(row[0])
#
#  region = 'EMEA'
#
#  for i in range(1-1,13):
#
#    c.execute \
#      ( \
#        '''
#          SELECT work_type, SUM(hours) AS total
#          FROM timesheets AS ts
#          WHERE region = ? and (ts.entry_date >= ? and ts.entry_date < ?)
#          GROUP BY work_type
#        ''', (region,week[i],week[i+1]))
#
#    wid = [(4,'L','act'),(6,'R','total')]
#
#    logging.debug('Week ' + str(i+1) + ' ' + week[i])
#    for row in c.fetchall():
#      index = 0
#      text = '|'
#      for col in row:
#        w = wid[index][0]
#        if (col is None):
#          col = ''
#        col = str(col)
#        if (len(col) > w): col = col[:w]
#        text += col.ljust(w) + '|'
#        index += 1
#      logging.debug(text)
#
#    logging.debug('')
#
#'''