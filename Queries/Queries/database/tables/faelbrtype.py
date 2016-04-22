import logging
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class FaeLaborTypeTable(Table):
  def __init__(self):
    pass

  def Create(self,db,lbrtypes):

    c = db.cursor()

    try:
      c.execute('DROP TABLE fae_lbrtype')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE fae_lbrtype
             (
               key         TEXT UNIQUE PRIMARY KEY,
               desc        TEXT
             )
        '''
      )

    c.executemany('INSERT INTO fae_lbrtype VALUES (?,?)',lbrtypes)
    db.commit()
