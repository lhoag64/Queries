import logging
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class FaeRegionTable(Table):
  def __init__(self):
    pass

  def Create(self,db,regions):

    c = db.cursor()

    try:
      c.execute('DROP TABLE fae_region')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE fae_region
             (
               key         TEXT UNIQUE PRIMARY KEY,
               desc        TEXT
             )
        '''
      )

    c.executemany('INSERT INTO fae_lbrtype VALUES (?,?)',regions)
    db.commit()
