import logging
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class FaePrdTeamTable(Table):
  def __init__(self):
    pass

  def Create(self,db,prdteams):

    c = db.cursor()

    try:
      c.execute('DROP TABLE fae_prdtm')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE fae_prdtm
             (
               key         TEXT UNIQUE PRIMARY KEY,
               desc        TEXT
             )
        '''
      )

    c.executemany('INSERT INTO fae_prdtm VALUES (?,?)',prdteams)
    db.commit()
