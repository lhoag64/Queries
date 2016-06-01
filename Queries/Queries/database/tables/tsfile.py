import logging
import os.path
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsFileTable(Table):
  def __init__(self):
    pass

  #--------------------------------------------------------------------
  def Create(self,db):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_file')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_file
             (
               file        TEXT UNIQUE PRIMARY KEY
             )
        '''
      )

    db.commit()

  #--------------------------------------------------------------------
  def Insert(self,db,tsdata):

    tsfiles = set([])

    c = db.cursor()
    c.execute('SELECT * FROM ts_file')
    for val in c.fetchall():
      tsfiles.add(val)

  
    tsDict = tsdata.tsdict
 
    files = set([])
    for week in tsDict:
      if (tsDict[week] != None):
        for name in tsDict[week]:  
          filename = os.path.basename(tsDict[week][name].filename)
          if (filename not in tsfiles):
            if (filename not in files):
              files.add(filename)
            else:
              logging.warn('Duplicate file found: ' + filename)
          else:
            logging.warn('Duplicate file found: ' + filename)

    filelist = list(files)

    if (len(filelist) > 0):
      c = db.cursor()
      for file in filelist:
        try:
          c.execute('INSERT INTO ts_file VALUES (?)',(file,))
        except sqlite3.IntegrityError:
          logging.debug(file)
    
      db.commit()
