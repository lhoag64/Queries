import logging
from   database.database                 import Database as Db
from   summary.matrix.actvitivydata      import ActivityData
from   summary.matrix.actvitivyamdmrdata import ActivityAmDmrData
from   summary.matrix.actvitivyammidata  import ActivityAmMiData
from   summary.matrix.ltsdata            import LtsData
from   summary.matrix.utlcfdata          import UtlCfData
from   summary.matrix.utlpsdata          import UtlPsData
from   summary.matrix.utldtdata          import UtlDtData
from   summary.matrix.utllsdata          import UtlLsData
from   summary.matrix.overtimedata       import OverTimeData
from   summary.matrix.gkadata            import GkaData
from   summary.matrix.amrkadata          import AmRkaData
from   summary.matrix.amtmcardata        import AmTmCarData
from   summary.matrix.amtmsmcdata        import AmTmSmcData
from   summary.matrix.ammirkadata        import AmMiRkaData
from   summary.matrix.actbylocdata       import ActByLocData
from   summary.matrix.actbyprdteamdata   import ActByPrdTeamData
from   summary.matrix.faeawhdata         import FaeAwhData
from   summary.matrix.faewhdata          import FaeWhData
from   summary.matrix.faeltdata          import FaeLtData
from   summary.matrix.faeotdata          import FaeOtData

#----------------------------------------------------------------------
class MatrixData:
  #--------------------------------------------------------------------
  def __init__(self,region,type,period,**kwargs):
    self.region = region
    self.type   = type
    self.period = period
    self.table  = None

    if (type == 'ACTIVITY'):
      self.table = ActivityData(region,type,period)
    elif (type == 'ACTIVITY-AM-DMR'):
      self.table = ActivityAmDmrData(region,type,period)
    elif (type == 'ACTIVITY-AM-MI'):
      self.table = ActivityAmMiData(region,type,period)
    elif (type == 'LTS'):
      self.table = LtsData(region,type,period)
    elif (type == 'UTL-CF'):
      self.table = UtlCfData(region,type,period)
    elif (type == 'UTL-PS'):
      self.table = UtlPsData(region,type,period)
    elif (type == 'UTL-DT'):
      self.table = UtlDtData(region,type,period)
    elif (type == 'UTL-LS'):
      self.table = UtlLsData(region,type,period)
    elif (type == 'OVERTIME'):
      self.table = OverTimeData(region,type,period)
    elif (type == 'GKA'):
      self.table = GkaData(region,type,period)
    elif (type == 'ACT-BY-LOC'):
      self.table = ActByLocData(region,type,period,**kwargs)
    elif (type == 'ACT-BY-PRD-TEAM'):
      self.table = ActByPrdTeamData(region,type,period,**kwargs)
    elif (type == 'AM-RKA'):
      self.table = AmRkaData(region,type,period)
    elif (type == 'AM-TM-CAR'):
      self.table = AmTmCarData(region,type,period)
    elif (type == 'AM-TM-SMC'):
      self.table = AmTmSmcData(region,type,period)
    elif (type == 'AM-TM-SMC'):
      self.table = AmTmSmcData(region,type,period)
    elif (type == 'AM-MI-RKA'):
      self.table = AmMiRkaData(region,type,period)
    elif (type == 'FAE-AWH'):
      self.table = FaeAwhData(region,type,period)
    elif (type == 'FAE-WH'):
      self.table = FaeWhData(region,type,period)
    elif (type == 'FAE-LT'):
      self.table = FaeLtData(region,type,period)
    elif (type == 'FAE-OT'):
      self.table = FaeOtData(region,type,period)

