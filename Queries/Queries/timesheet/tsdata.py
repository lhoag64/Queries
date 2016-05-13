import logging
from timesheet.calendar   import Calendar
from timesheet.timesheet  import Timesheet

#-----------------------------------------------------------------------
class TsData:
  #region = None
  #team   = None
  #weeks  = None

  def __init__(self,region,team,weeks,flData):
    self.region  = region
    self.team    = team
    self.weeks   = weeks

    tslist      = self.GetFileList(flData,weeks,region)
    self.tsdict = self.ReadTimesheets(tslist)

  #---------------------------------------------------------------------
  def GetFileList(self,flData,weeks,region):
    tslist = []
    for i in weeks:
      list = []
      dict = {}
      wsDate = Calendar.week[i]
      if (wsDate in flData.weeks):
        logging.debug('Building ' + region + ' Filelist for week ' + str(i+1).rjust(2) + ' ' + str(wsDate))
        dict = flData.weeks[wsDate]
        for key,value in dict.items():
          list.append(value)
        tslist.append(sorted(list))
      else:
        logging.debug('Skipping ' + region + ' Filelist for week ' + str(i+1).rjust(2) + ' ' + str(wsDate))

    return tslist

  #---------------------------------------------------------------------
  def ReadTimesheets(self,tslist):
    tsdict = {}
    for i,week in enumerate(tslist):
      wsDate = Calendar.week[self.weeks[i]]
      tsdict[wsDate] = []
      for j,tsdate in enumerate(week):
        ts = Timesheet(tsdate,wsDate)
        ts.ReadFile()
        tsdict[wsDate].append(ts)

    return tsdict
