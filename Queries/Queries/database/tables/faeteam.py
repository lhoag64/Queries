import logging
import sqlite3
from   database.tables.table   import Table
from   database.tables.faedata import FaeTeam

#----------------------------------------------------------------------
class FaeTeamTable(Table):
  def __init__(self):
    pass

  def Create(self,db):

    c = db.cursor()

    try:
      c.execute('DROP TABLE fae_team')
    except sqlite3.OperationalError:
      pass


    c.execute('SELECT key,desc FROM fae_region')
    regions = c.fetchall()
    c.execute('SELECT key,desc FROM fae_prdtm')
    prdteams = c.fetchall()
    c.execute('SELECT key,desc FROM fae_lbrtype')
    lbrtypes = c.fetchall()
    c.execute('SELECT key,desc FROM fae_loc')
    locs = c.fetchall()

    c.execute \
      ( \
        '''
           CREATE TABLE fae_team
             (
               fname       TEXT,
               fnalias     TEXT,
               lname       TEXT,
               lnalias     TEXT,
               region      TEXT,
               lbr_type    TEXT,    
               prd_team    TEXT,    
               fae_loc     TEXT,    
               norm_hours  NUMERIC,
               max_hours   NUMERIC,
               start_date  DATE,
               end_date    DATE,
               FOREIGN KEY (region)  REFERENCES fae_region(key),
               FOREIGN KEY (lbr_type) REFERENCES fae_lbrtype(key),
               FOREIGN KEY (prd_team) REFERENCES fae_prdteam(key),
               FOREIGN KEY (fae_loc) REFERENCES fae_loc(key)
             )
        '''
      )

    rows = []
    team = FaeTeam()
    for fae in team.faes:
      fname      = fae.fname
      lname      = fae.lname
      fnalias    = fae.fnalias
      lnalias    = fae.lnalias
      region     = fae.region
      lbrtype    = fae.lbrType
      prdteam    = fae.prdTeam
      loc        = fae.loc
      norm_hours = fae.normHours
      max_hours  = fae.maxHours
      start_date = fae.startDate
      end_date   = fae.endDate

      row = \
        ( \
          fname,fnalias,lname,lnalias,region,lbrtype, \
          prdteam,loc,norm_hours,max_hours,start_date,end_date \
        )
      rows.append(row)

    c.executemany('INSERT INTO fae_team VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',rows)
    db.commit()

  