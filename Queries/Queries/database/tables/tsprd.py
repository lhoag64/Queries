import logging
import re
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsPrdTable(Table):
  def __init__(self):
    pass

  def Create(self,db,list):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_prd')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_prd
             (
               prd          INTEGER UNIQUE PRIMARY KEY,
               desc         TEXT
             )
        '''
      )

    products = set([])
    rows = []
    for item in list:
      matches = []
      for match in re.finditer('[-|–]',item):
        matches.append((match.start(),match.end()))
      if (len(matches) == 0):
        logging.error('Can\'t find \'-\' in Code string:\'' + item + '\'')
        continue
      loc      = matches[-1]
      product  = int(item[loc[1]:].strip())
      desc     = item[:loc[0]].strip()

      if (product not in products):
        products.add(product)
      else:
        logging.error('Activity is already used:\'' + item + '\',skipping')
        continue

      row = (product,desc)
      rows.append(row)

    c.executemany('INSERT INTO ts_prd VALUES (?,?)',rows)

    db.commit()
 