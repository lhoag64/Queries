import logging
from xlinterface.xlworkbook  import XlWorkBook
from xlinterface.xlworksheet import XlWorkSheet

#----------------------------------------------------------------------
class Fae:

  Regions      = [('AM','Americas'),('EMEA','Europe/Middle East'),('GC','Greater China'),('ROAPAC','Rest of APAC'),('BU','Business Unit')]
  ProductTeams = [('DMR','Digital Mobile Radio'),('MI','Modular Instruments'),('TVM','TeraVM'),('DAS','Coverage')]
  LaborTypes   = [('P','Direct Hire'),('C','Contractor')]
  Locatons     = [('N','North'),('S','South'),('E','East'),('W','West'),('R','Regional'), \
                  ('UK','United Kindom'),('SE','Sweden'),('FI','Finland'),('FR','France'),('DE','Germany'), \
                  ('IN','India'),('JP','Japan'),('KO','Korea'),('SG','Singapore'),('AU','Austrailia') \
                 ]

  def __init__(self,region,fname,fnalias,lname,lnalias,laborType,prodTeam,location,normHours,maxHours,startDate,endDate):
    self.region    = region
    self.fname     = fname
    self.fnalias   = fnalias
    self.lname     = lname
    self.lnalias   = lnalias
    self.lbrType   = laborType
    self.prdTeam   = prodTeam
    self.loc       = location
    self.normHours = normHours
    self.maxHours  = maxHours
    self.startDate = startDate
    self.endDate   = endDate

class FaeTeam:
  def __init__(self):
    faelist = []

    # TODO: Remove hardcoded pathname
    wb = XlWorkBook()
    wb.Read(r'X:\Reporting\Timesheets\Global-FAEs.xlsx')

    ws = wb.GetSheetByName('FAEs')

    wsRow = 2
    wsCol = 1

    while (1):
      region  = ws.GetValue(wsRow,wsCol+ 0)
      if (region == None):
        break
      region  = region.strip()
      fname   = ws.GetValue(wsRow,wsCol+ 1).strip()
      if (ws.GetValue(wsRow,wsCol+ 2) != None):
        fnalias = ws.GetValue(wsRow,wsCol+ 2).strip()
      else:
        fnalias = None
      lname   = ws.GetValue(wsRow,wsCol+ 3).strip()
      if (ws.GetValue(wsRow,wsCol+ 4) != None):
        lnalias = ws.GetValue(wsRow,wsCol+ 4).strip()
      else:
        lnalias = None
      lbrType = ws.GetValue(wsRow,wsCol+ 5).strip()
      prdTeam = ws.GetValue(wsRow,wsCol+ 6).strip()
      loc     = ws.GetValue(wsRow,wsCol+ 7).strip()
      normHrs = ws.GetValue(wsRow,wsCol+ 8)
      maxHrs  = ws.GetValue(wsRow,wsCol+ 9)
      start   = ws.GetValue(wsRow,wsCol+10)
      end     = ws.GetValue(wsRow,wsCol+11)

      normHrs = float(normHrs)
      maxHrs  = float(maxHrs)
      start   = str(start)[:10]
      end     = str(end)[:10]

      faelist.append(Fae(region,fname,fnalias,lname,lnalias,lbrType,prdTeam,loc,normHrs,maxHrs,start,end))
      wsRow += 1

    self.faes = faelist

