import logging
import re
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsActTable(Table):
  def __init__(self):
    pass

  #--------------------------------------------------------------------
  def Create(self,db,list):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_act')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_act
             (
               act          INTEGER UNIQUE PRIMARY KEY,
               desc         TEXT,
               billable     INTEGER,
               pre_sales    INTEGER,
               non_bill     INTEGER,
               standard     INTEGER
             )
        '''
      )

    activities = set([])
    rows = []
    for item in list:
      matches = []
      for match in re.finditer('[-|–]',item):
        matches.append((match.start(),match.end()))
      if (len(matches) == 0):
        logging.error('Can\'t find \'-\' in Code string:\'' + item + '\'')
        continue
      loc      = matches[-1]
      activity = int(item[loc[1]:].strip())
      desc     = item[:loc[0]].strip()

      billable    = 0
      nonBillable = 0
      preSales    = 0
      if (activity in set([10,11,14,15,16,17,18])):
        billable    = 1
      if (activity in set([12,13,19,20,21,22])):
        preSales    = 1
      if (not billable and not preSales):
        nonBillable = 1

      standard = 1

      if (activity not in activities):
        activities.add(activity)
      else:
        logging.error('Activity is already used:\'' + item + '\',skipping')
        continue

      row = (activity,desc,billable,preSales,nonBillable,standard)
      rows.append(row)

    #activities.add((99,'Other (Leave, Overhead, etc)',0,0,0,0))

    c.executemany('INSERT INTO ts_act VALUES (?,?,?,?,?,?)',rows)

    db.commit()
 

