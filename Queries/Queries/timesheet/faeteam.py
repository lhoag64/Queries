import logging
import sqlite3
from   timesheet.calendar import Calendar
from   database           import Database as Db

#----------------------------------------------------------------------
class Fae:
  def __init__(self,data):
    self.fname     = data[ 0]
    self.fnalias   = []
    if (len(data[1]) > 0):
      stxt = data[1].split(',')
      for name in stxt:
        self.fnalias.append(name)
    self.lname     = data[ 2]
    self.lnalias   = []
    if (len(data[3]) > 0):
      stxt = data[3].split(',')
      for name in stxt:
        self.lnalias.append(name)
    self.fullname  = self.fname + ' ' + self.lname
    self.region    = data[ 4]
    self.lbrType   = data[ 5]
    self.prdTeam   = data[ 6]
    self.location  = data[ 7]
    self.normHours = data[ 8]
    self.maxHours  = data[ 9]
    self.startDate = Calendar.StrToDate(str(data[10]))
    self.endDate   = Calendar.StrToDate(str(data[11]))

  def __lt__(self,other):
    if (self.prdTeam != other.prdTeam):
      if (self.prdTeam < other.prdTeam):
        return True
      else:
        return False
    elif (self.location != other.location):
      if (self.location < other.location):
        return True
      else:
        return False
    elif (self.lname != other.lname):
      if (self.lname < other.lname):
        return True
      else:
        return False
    elif (self.fname != other.fname):
      if (self.fname < other.fname):
        return True
      else:
        return False
    logging.error('SHOULD NOT BE HERE')
    return False

#----------------------------------------------------------------------
class FaeTeam:
  dict = {}
  list = []
  def __init__(self,region=None):
    self.dict = {}
    self.list = []

    # TODO: Let Db do query

    db = Db.GetDb()
    c = db.cursor()
    if (not region):
      c.execute('SELECT * FROM fae_team')
    else:
      c.execute('SELECT * FROM fae_team WHERE region=?',(region,))
    values = c.fetchall()
    for val in values:
      fullname = val[0] + ' ' + val[2]
      self.dict[fullname] = Fae(val)

    self.list = sorted(self.dict.values())



