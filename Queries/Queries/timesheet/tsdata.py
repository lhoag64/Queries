import logging
import datetime
from collections          import OrderedDict
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

    tsDict      = self.GetFileList(flData,weeks,region)
    self.tsdict = self.ReadTimesheets(tsDict)

  #---------------------------------------------------------------------
  def GetFileList(self,flData,weeks,region):
    tsDict = OrderedDict()
    now = datetime.date.today().strftime("%Y-%m-%d")
    week = Calendar.GetWeek(now)
    for idx in range(1,week):
      tsDict[Calendar.week[idx]] = None

    for i in weeks:
      wsDate = Calendar.week[i]
      if (wsDate in flData.weeks):
        if (flData.weeks[wsDate] != None):
          tsDict[wsDate] = OrderedDict()
          for item in flData.weeks[wsDate]:
            tsDict[wsDate][item] = flData.weeks[wsDate][item]
        else:
          logging.debug('Skipping ' + region + ' Filelist for week ' + str(i).rjust(2) + ' - ' + str(wsDate))

#        logging.debug('Building ' + region + ' Filelist for week ' + str(i+1).rjust(2) + ' ' + str(wsDate))
#        dict = flData.weeks[wsDate]
#        for key,value in dict.items():
#          list.append(value)
#        tslist.append(sorted(list))
#      else:
#        logging.debug('Skipping ' + region + ' Filelist for week ' + str(i+1).rjust(2) + ' ' + str(wsDate))

    return tsDict

  #---------------------------------------------------------------------
  def ReadTimesheets(self,tsDict):
    for wsDate in tsDict:
      faeDict = tsDict[wsDate]
      if (faeDict):
        for name in faeDict:
          ts = Timesheet(faeDict[name],wsDate)
          ts.ReadFile()
          tsDict[wsDate][name].timeSheet = ts

    return tsDict
