import logging
from   database.database            import Database as Db
from   summary.matrix.actvitivydata import ActivityData
from   summary.matrix.ltsdata       import LtsData
from   summary.matrix.utlcfdata     import UtlCfData
from   summary.matrix.utlpsdata     import UtlPsData
from   summary.matrix.utldtdata     import UtlDtData
from   summary.matrix.utllsdata     import UtlLsData
from   summary.matrix.overtimedata  import OverTimeData
from   summary.matrix.gkadata       import GkaData
from   summary.matrix.actbylocdata  import ActByLocData
from   summary.matrix.faeawhdata    import FaeAwhData
from   summary.matrix.faewhdata     import FaeWhData

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
    elif (type == 'FAE-AWH'):
      self.table = FaeAwhData(region,type,period)
    elif (type == 'FAE-WH'):
      self.table = FaeWhData(region,type,period)

