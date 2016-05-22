import logging
import re
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsCodeTable(Table):
  def __init__(self):
    pass

  def Create(self,db,list):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_code')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_code
             (
               code                 TEXT UNIQUE PRIMARY KEY,
               desc                 TEXT,
               downtime             INTEGER,
               leave                INTEGER,
               gl_tm_key_acct       INTEGER,
               gl_tm_key_acct_order INTEGER,
               am_tm_car_acct       INTEGER,
               am_tm_smc_acct       INTEGER,
               am_mi_rka_acct       INTEGER
             )
        '''
      )

    codes = set([])
    rows = []
    for item in list:
      matches = []
      for match in re.finditer('[-|–]',item):
        matches.append((match.start(),match.end()))
      if (len(matches) == 0):
        if (item.find('DOWNTIME CODES') < 0):
          logging.error('Can\'t find \'-\' in Code string:\'' + item + '\'')
        continue
      loc = matches[-1]
      code = item[loc[1]:].strip()
      desc = item[:loc[0]].strip()

      if (code not in codes):
        codes.add(code)
      else:
        logging.error('Code is already used:\'' + item + '\',skipping')
        continue

      downtime       =   0
      leave          =   0
      gka            =   0
      gka_order      = 100
      am_tm_car_acct =   0
      am_tm_smc_acct =   0
      am_mi_key_acct =   0

# downtime - 4804,4807,4803,4901,1006

      if (len(code) == 5):
        if (code[:1] == 'X'):
          if (code in ['X4804','X4807','X4803','X4901','X1006']):
            downtime = 1
          else:
            leave = 1
        else:
          logging.error('Invalid Code:' + code)
      elif (len(code) == 3):
        if (code in ['ERC','NOK','NSN','ALU','ASB','TTT','COB','OTH']):
          gka = 1
          if (code == 'ERC'):
            gka_order = 0
          elif (code == 'NOK'):
            gka_order = 1
          elif (code == 'ALU'):
            gka_order = 2
          elif (code == 'COB'):
            gka_order = 5
          elif (code == 'TTT'):
            gka_order = 6
          elif (code == 'OTH'):
            gka_order = 7
          else:
            gka_order = 99
        if (code in ['ATT','TMO','SPR']):
          am_tm_car_acct = 1
        if (code in ['QUA','INT']):
          am_tm_smc_acct = 1
        if (code in ['QOR','TER','SKY']):
          am_mi_key_acct = 1

      row = (code,desc,downtime,leave,gka,gka_order,am_tm_car_acct,am_tm_smc_acct,am_mi_key_acct)
      rows.append(row)

    c.executemany('INSERT INTO ts_code VALUES (?,?,?,?,?,?,?,?,?)',rows)

    db.commit()


