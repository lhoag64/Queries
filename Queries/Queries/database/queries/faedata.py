import logging

#----------------------------------------------------------------------
class FaeWorkingDays:
  def __init__(self):
    self.weekNum = None
    self.am_days = None
    self.uk_days = None
    self.fr_days = None
    self.de_days = None
    self.se_days = None
    self.gc_days = None

#----------------------------------------------------------------------
class FaeData:
  def __init__(self,fname,lname,nrmHrs,maxHrs,lbrType,startDate,endDate,region):
    self.fname     = fname
    self.lname     = lname
    self.nrmHrs    = nrmHrs
    self.maxHrs    = maxHrs
    self.lbrType   = lbrType
    self.startDate = startDate
    self.endDate   = endDate
    self.region    = region

#----------------------------------------------------------------------
class FaeHoursData:
  def __init__(self,workingDays,hc,hours):
    self.workingDays = workingDays
    self.headCount   = hc
    self.hours       = hours

#----------------------------------------------------------------------
class FaeSumData:
  def __init__(self,faeList,hoursList):
    self.faeList   = faeList
    self.hoursList = hoursList

