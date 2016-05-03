import os.path
import logging
import sqlite3
from   database.tables.faedata     import Fae
from   database.tables.masterts    import Master
from   database.tables.faelbrtype  import FaeLaborTypeTable
from   database.tables.faeloc      import FaeLocTable
from   database.tables.faeprdteam  import FaePrdTeamTable
from   database.tables.faeregion   import FaeRegionTable
from   database.tables.faeteam     import FaeTeamTable
from   database.tables.tscode      import TsCodeTable
from   database.tables.tsloc       import TsLocTable
from   database.tables.tsact       import TsActTable
from   database.tables.tsprd       import TsPrdTable
from   database.tables.tslts       import TsLtsTable
from   database.tables.tsfile      import TsFileTable
from   database.tables.tsentry     import TsEntryTable
from   database.tables.weeks       import WeeksTable



#----------------------------------------------------------------------
class Database:
  def __init__(self):
    Database.db          = None
    Database.root        = None
    Database.filename    = None
    Database.masterts    = None

    Database.FaeLbrTbl   = FaeLaborTypeTable()
    Database.FaeLocTbl   = FaeLocTable()
    Database.FaePrdTmTbl = FaePrdTeamTable()
    Database.FaeRgnTbl   = FaeRegionTable()
    Database.FaeTmTbl    = FaeTeamTable()
    Database.TsCodeTbl   = TsCodeTable()
    Database.TsLocTbl    = TsLocTable()
    Database.TsActTbl    = TsActTable()
    Database.TsPrdTbl    = TsPrdTable()
    Database.TsLtsTbl    = TsLtsTable()
    Database.TsFileTbl   = TsFileTable()
    Database.TsEntryTbl  = TsEntryTable()
    Database.WeeksTbl    = WeeksTable()

  #--------------------------------------------------------------------
  def GetDb():
    return Database.db

  #--------------------------------------------------------------------
  def Connect(root,filename):
    Database.root     = root
    Database.filename = filename

    pathname = os.path.join(root,filename)
    Database.db = sqlite3.connect(pathname)

  #--------------------------------------------------------------------
  def CreateTables(list):
    for item in list:
      if   (item == 'fae_lbrtype'): Database.createFaeLbrTbl()
      elif (item == 'fae_loc'    ): Database.createFaeLocTbl()
      elif (item == 'fae_prdtm'  ): Database.createFaePrdTmTbl()
      elif (item == 'fae_region' ): Database.createFaeRgnTbl()
      elif (item == 'fae_team'   ): Database.createFaeTmTbl()
      elif (item == 'ts_code'    ): Database.createTsCodeTbl()
      elif (item == 'ts_loc'     ): Database.createTsLocTbl()
      elif (item == 'ts_act'     ): Database.createTsActTbl()
      elif (item == 'ts_prd'     ): Database.createTsPrdTbl()
      elif (item == 'ts_lts'     ): Database.createTsLtsTbl()
      elif (item == 'ts_file'    ): Database.createTsFileTbl()
      elif (item == 'ts_entry'   ): Database.createTsEntryTbl()
      elif (item == 'weeks'      ): Database.createWeeksTbl()

  #--------------------------------------------------------------------
  def InsertTimesheets(tsdata):
    Database.TsFileTbl.Insert(Database.db,tsdata)
    Database.TsEntryTbl.Insert(Database.db,tsdata)

  #--------------------------------------------------------------------
  def createFaeLbrTbl():
    Database.FaeLbrTbl.Create(Database.db,Fae.LaborTypes)

  #--------------------------------------------------------------------
  def createFaeLocTbl():
    Database.FaeLocTbl.Create(Database.db,Fae.Locatons)

  #--------------------------------------------------------------------
  def createFaePrdTmTbl():
    Database.FaePrdTmTbl.Create(Database.db,Fae.ProductTeams)

  #--------------------------------------------------------------------
  def createFaeRgnTbl():
    Database.FaeRgnTbl.Create(Database.db,Fae.Regions)

  #--------------------------------------------------------------------
  def createFaeTmTbl():
    Database.FaeTmTbl.Create(Database.db)

  #--------------------------------------------------------------------
  def createTsCodeTbl():
    if (not Database.masterts): Database.masterts = Master(Database.root)
    Database.TsCodeTbl.Create(Database.db,Database.masterts.data['CODES'])

  #--------------------------------------------------------------------
  def createTsLocTbl():
    if (not Database.masterts): Database.masterts = Master(Database.root)
    Database.TsLocTbl.Create(Database.db,Database.masterts.data['LOCATIONS'])

  #--------------------------------------------------------------------
  def createTsActTbl():
    if (not Database.masterts): Database.masterts = Master(Database.root)
    Database.TsActTbl.Create(Database.db,Database.masterts.data['ACTIVITIES'])

  #--------------------------------------------------------------------
  def createTsPrdTbl():
    if (not Database.masterts): Database.masterts = Master(Database.root)
    Database.TsPrdTbl.Create(Database.db,Database.masterts.data['PRODUCTS'])

  #--------------------------------------------------------------------
  def createTsLtsTbl():
    Database.TsLtsTbl.Create(Database.db)

  #--------------------------------------------------------------------
  def createTsFileTbl():
    Database.TsFileTbl.Create(Database.db)

  #--------------------------------------------------------------------
  def createTsEntryTbl():
    Database.TsEntryTbl.Create(Database.db)

  #--------------------------------------------------------------------
  def createWeeksTbl():
    Database.WeeksTbl.Create(Database.db)

