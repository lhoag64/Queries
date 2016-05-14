import logging
import sqlite3

#----------------------------------------------------------------------
def GetLts(db,type):

  c = db.cursor()
  c.execute(' SELECT key FROM ts_lts')
  ltslist = c.fetchall()

  return ltslist
