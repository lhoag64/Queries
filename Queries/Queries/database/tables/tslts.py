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
