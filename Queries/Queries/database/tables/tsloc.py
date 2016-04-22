import logging
import re
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsLocTable(Table):
  def __init__(self):
    pass

  def Create(self,db,list):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_loc')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_loc
             (
               loc          INTEGER UNIQUE PRIMARY KEY,
               desc         TEXT
             )
        '''
      )

    locations = set([])
    rows = []
    for item in list:
      matches = []
      for match in re.finditer('[-|–]',item):
        matches.append((match.start(),match.end()))
      if (len(matches) == 0):
        logging.error('Can\'t find \'-\' in Code string:\'' + item + '\'')
        continue
      loc      = matches[-1]
      location = int(item[loc[1]:].strip())
      desc     = item[:loc[0]].strip()

      if (location not in locations):
        locations.add(location)
      else:
        logging.error('Location is already used:\'' + item + '\',skipping')
        continue

      row = (location,desc)
      rows.append(row)

    c.executemany('INSERT INTO ts_loc VALUES (?,?)',rows)

    db.commit()



