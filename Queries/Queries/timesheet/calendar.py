import datetime
import logging

#calendar = None

#-----------------------------------------------------------------------
class Calendar:

  week    = {}
  revWeek = None
  wsDates = None
  weDates = None

  def StrToDate(text):
    year = int(text[0: 4])
    mon  = int(text[5: 7])
    day  = int(text[8:10])
    return datetime.date(year,mon,day)


  def __init__(self,year):
    Calendar.week = {}
    Calendar.wsDates = set()
    Calendar.weDates = set()

    d = datetime.date(year,1,1)
    while (True):
      if (d.weekday() == 0):
        break;
      else:
        d = d + datetime.timedelta(days=1)
    i = 1
    while(True):
      Calendar.week[i] = d
      Calendar.wsDates.add(d)
      Calendar.weDates.add(d+datetime.timedelta(days=6))
      d = d + datetime.timedelta(days=7)
      if (d.year > year):
        break;
      i += 1
    Calendar.revWeek = {v:k for k,v in Calendar.week.items()}
    pass

  def GetWsDate(week):
    return Calendar.week[week]
 
  def GetWeDate(week):
    return Calendar.week[week] + datetime.timedelta(days=6)

  def GetWeek(date):
    curDate = Calendar.StrToDate(date)
    day = curDate.weekday()
    wcDate = curDate + datetime.timedelta(days=(7-day))
    week = Calendar.revWeek[wcDate]
    return week
 
