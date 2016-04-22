import logging
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class FaeLocTable(Table):
  def __init__(self):
    pass

  def Create(self,db,locations):

    c = db.cursor()

    try:
      c.execute('DROP TABLE fae_loc')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE fae_loc
             (
               key         TEXT UNIQUE PRIMARY KEY,
               desc        TEXT
             )
        '''
      )

    c.executemany('INSERT INTO fae_loc VALUES (?,?)',locations)
    db.commit()