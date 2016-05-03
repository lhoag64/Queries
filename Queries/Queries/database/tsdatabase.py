#import os.path
#import logging
#import sqlite3
#from   database.tables.faedata     import Fae
#from   database.tables.masterts    import Master
#from   database.tables.faelbrtype  import FaeLaborTypeTable
#from   database.tables.faeloc      import FaeLocTable
#from   database.tables.faeprdteam  import FaePrdTeamTable
#from   database.tables.faeregion   import FaeRegionTable
#from   database.tables.faeteam     import FaeTeamTable
#from   database.tables.tscode      import TsCodeTable
#from   database.tables.tsloc       import TsLocTable
#from   database.tables.tsact       import TsActTable
#from   database.tables.tsprd       import TsPrdTable
#from   database.tables.tslts       import TsLtsTable
#from   database.tables.tsfile      import TsFileTable
#from   database.tables.tsentry     import TsEntryTable
#from   database.tables.weeks       import WeeksTable
#
#----------------------------------------------------------------------
#class TsDatabase:
#  def __init__(self):
#    self.tblDict       = {}
#    self.root          = None
#    self.dbname        = None
#    self.masterts      = None
#    self.faeLbrTypeTbl = FaeLaborTypeTable()
#    self.faeLocTbl     = FaeLocTable()
#    self.faePrdTmTbl   = FaePrdTeamTable()
#    self.faeRgnTbl     = FaeRegionTable()
#    self.faeTmTbl      = FaeTeamTable()
#    self.tsCodeTbl     = TsCodeTable()
#    self.tsLocTbl      = TsLocTable()
#    self.tsActTbl      = TsActTable()
#    self.tsPrdTbl      = TsPrdTable()
#    self.tsLtsTbl      = TsLtsTable()
#    self.tsFileTbl     = TsFileTable()
#    self.tsEntryTbl    = TsEntryTable()
#    self.weeksTbl      = WeeksTable()
#
#    self.tblDict['fae_lbrtype'] = self.faeLbrTypeTbl
#    self.tblDict['fae_loc'    ] = self.faeLocTbl
#    self.tblDict['fae_prdtm'  ] = self.faePrdTmTbl
#    self.tblDict['fae_region' ] = self.faeRgnTbl
#    self.tblDict['fae_team'   ] = self.faeTmTbl
#    self.tblDict['ts_code'    ] = self.tsCodeTbl
#    self.tblDict['ts_loc'     ] = self.tsLocTbl
#    self.tblDict['ts_act'     ] = self.tsActTbl
#    self.tblDict['ts_prd'     ] = self.tsPrdTbl
#    self.tblDict['ts_lts'     ] = self.tsLtsTbl
#    self.tblDict['ts_file'    ] = self.tsFileTbl
#    self.tblDict['ts_entry'   ] = self.tsEntryTbl
#    self.tblDict['weeks'      ] = self.weeksTbl
#
#  #--------------------------------------------------------------------
#  def Connect(self,root,dbname):
#    self.root = root
#    self.dbname = dbname
#
#    filename = os.path.join(root,dbname)
#    self.db = sqlite3.connect(filename)
#    return self.db
#
#  #--------------------------------------------------------------------
#  def CreateTables(self,list):
#    for item in list:
#      if   (item == 'fae_lbrtype'): self.createFaeLbrTypeTbl()
#      elif (item == 'fae_loc'    ): self.createFaeLocTbl()
#      elif (item == 'fae_prdtm'  ): self.createFaePrdTmTbl()
#      elif (item == 'fae_region' ): self.createFaeRgnTbl()
#      elif (item == 'fae_team'   ): self.createFaeTmTbl()
#      elif (item == 'ts_code'    ): self.createTsCodeTbl()
#      elif (item == 'ts_loc'     ): self.createTsLocTbl()
#      elif (item == 'ts_act'     ): self.createTsActTbl()
#      elif (item == 'ts_prd'     ): self.createTsPrdTbl()
#      elif (item == 'ts_lts'     ): self.createTsLtsTbl()
#      elif (item == 'ts_file'    ): self.createTsFileTbl()
#      elif (item == 'ts_entry'   ): self.createTsEntryTbl()
#      elif (item == 'weeks'      ): self.createWeeksTbl()
#
#  #--------------------------------------------------------------------
#  def InsertTimesheets(self,tsdata):
#    self.tsFileTbl.Insert(self.db,tsdata)
#    self.tsEntryTbl.Insert(self.db,tsdata)
#
#  #--------------------------------------------------------------------
#  def GetWeeks(self,period):
#    return self.weeksTbl.GetWeeks(self.db,period)
#
#  #--------------------------------------------------------------------
#  def GetActivities(self,type):
#    return self.tsActTbl.GetActivities(self.db,type)
#
#  #--------------------------------------------------------------------
#  def GetActivitySum(self,region,act,period):
#    return self.tsEntryTbl.GetActivitySum(self.db,region,act,period)
#
#  #--------------------------------------------------------------------
#  def GetLts(self,type):
#    return self.tsLtsTbl.GetLts(self.db,type)
#
#  #--------------------------------------------------------------------
#  def GetLtsSum(self,region,act,period):
#    return self.tsEntryTbl.GetLtsSum(self.db,region,act,period)
#
#  #--------------------------------------------------------------------
#  def GetUtlCfSum(self,region,period):
#    return self.tsEntryTbl.GetUtlCfSum(self.db,region,period)
#
#  #--------------------------------------------------------------------
#  def GetUtlPsSum(self,region,period):
#    return self.tsEntryTbl.GetUtlPsSum(self.db,region,period)
#
#  #--------------------------------------------------------------------
#  def GetUtlDtSum(self,region,period):
#    return self.tsEntryTbl.GetUtlDtSum(self.db,region,period)
#
#  #--------------------------------------------------------------------
#  def GetUtlLsSum(self,region,period):
#    return self.tsEntryTbl.GetUtlLsSum(self.db,region,period)
#
#  #--------------------------------------------------------------------
#  def GetOverTimeSum(self,region,period):
#    return self.tsEntryTbl.GetOverTimeSum(self.db,region,period)
#
#  #--------------------------------------------------------------------
#  def GetGkaSum(self,region,codes,period):
#    return self.tsEntryTbl.GetGkaSum(self.db,region,codes,period)
#
#  #--------------------------------------------------------------------
#  def GetActByLocSum(self,region,act,loc,period):
#    return self.tsEntryTbl.GetActByLocSum(self.db,region,act,loc,period)
#
#  #--------------------------------------------------------------------
#  def GetFaeAwhSum(self,region,period):
#    return self.tsEntryTbl.GetFaeAwhSum(self.db,region,period)
#
#  #--------------------------------------------------------------------
#  def createFaeLbrTypeTbl(self):
#    self.faeLbrTypeTbl.Create(self.db,Fae.LaborTypes)
#
#  #--------------------------------------------------------------------
#  def createFaeLocTbl(self):
#    self.faeLocTbl.Create(self.db,Fae.Locatons)
#
#  #--------------------------------------------------------------------
#  def createFaePrdTmTbl(self):
#    self.faePrdTmTbl.Create(self.db,Fae.ProductTeams)
#
#  #--------------------------------------------------------------------
#  def createFaeRgnTbl(self):
#    self.faeRgnTbl.Create(self.db,Fae.Regions)
#
#  #--------------------------------------------------------------------
#  def createFaeTmTbl(self):
#    self.faeTmTbl.Create(self.db)
#
#  #--------------------------------------------------------------------
#  def createTsCodeTbl(self):
#    if (not self.masterts): self.masterts = Master(self.root)
#    self.tsCodeTbl.Create(self.db,self.masterts.data['CODES'])
#
#  #--------------------------------------------------------------------
#  def createTsLocTbl(self):
#    if (not self.masterts): self.masterts = Master(self.root)
#    self.tsLocTbl.Create(self.db,self.masterts.data['LOCATIONS'])
#
#  #--------------------------------------------------------------------
#  def createTsActTbl(self):
#    if (not self.masterts): self.masterts = Master(self.root)
#    self.tsActTbl.Create(self.db,self.masterts.data['ACTIVITIES'])
#
#  #--------------------------------------------------------------------
#  def createTsPrdTbl(self):
#    if (not self.masterts): self.masterts = Master(self.root)
#    self.tsPrdTbl.Create(self.db,self.masterts.data['PRODUCTS'])
#
#  #--------------------------------------------------------------------
#  def createTsLtsTbl(self):
#    self.tsLtsTbl.Create(self.db)
#
#  #--------------------------------------------------------------------
#  def createTsFileTbl(self):
#    self.tsFileTbl.Create(self.db)
#
#  #--------------------------------------------------------------------
#  def createTsEntryTbl(self):
#    self.tsEntryTbl.Create(self.db)
#
#  #--------------------------------------------------------------------
#  def createWeeksTbl(self):
#    self.weeksTbl.Create(self.db)
#
#
#

