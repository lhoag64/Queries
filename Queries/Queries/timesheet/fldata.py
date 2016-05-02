import os
import os.path
import string
import datetime
import logging
import re
from   timesheet.calendar import Calendar
from   timesheet.faeteam  import FaeTeam

#-----------------------------------------------------------------------
class FlFile:
  def __init__(self,filename,team,estweek):
    self.fae      = None
    self.fname    = None
    self.lname    = None
    self.fullname = None
    self.filename = None
    self.weDate   = None
    self.wsDate   = None
    self.valid    = False

    fullpath = filename
    filename = os.path.basename(filename)

    while (1):
      for i in range(len(filename)):
        c = filename[i:i+1]
        o = ord(c)
        if (o > 127):
            index = i
            break
      if (o > 127):
        ltext = filename[:index-0]
        rtext = filename[index+1:]
        if (o == 8211):
          filename = ltext + '-' + rtext
        if (o == 8217):
          filename = ltext + '\'' + rtext
      else:
        break

    #text = '|' + filename + '|'
    #for i in range(len(filename)):
    #  c = filename[i:i+1]
    #  o = ord(c)
    #  if (o > 127):
    #    logging.error('Non-ascii character in filename: ' + filename)
    #  o = str(o).rjust(3)
    #  text += c + '-' + o + '|'
    #logging.debug(text)

    timesheet = re.compile('timesheet',re.IGNORECASE)
    match = timesheet.search(filename)
    if (not match):
      return

    #------------------------------------------------------------------
    # Try to figure out the name
    #------------------------------------------------------------------

    fae    = None
    valid  = False
    wsDate = None
    weDate = None

    lnameList   = []
    matchList   = []
    for fae in team.list:

      lnaliasList = []
      lnaliasList.append(fae.lname)
      for alias in fae.lnalias:
        lnaliasList.append(alias)

      for name in lnaliasList:
        nameRe = re.compile(name,re.IGNORECASE)
        match = nameRe.search(filename)
        if (match):
          lnameList.append(name)

    fnameList   = []
    for fae in team.list:

      fnaliasList = []
      fnaliasList.append(fae.fname)
      for alias in fae.fnalias:
        fnaliasList.append(alias)

      for name in fnaliasList:
        nameRe = re.compile(name,re.IGNORECASE)
        match = nameRe.search(filename)
        if (match):
          fnameList.append(name)

    faeFound = False
    index = 0
    for fae in team.list:
      lnMatch = 0
      fnMatch = 0

      lnaliasList = []
      lnaliasList.append(fae.lname)
      for alias in fae.lnalias:
        lnaliasList.append(alias)

      fnaliasList = []
      fnaliasList.append(fae.fname)
      for alias in fae.fnalias:
        fnaliasList.append(alias)

      for l in lnameList:
        possln = self.CapName(l)
        for lname in lnaliasList:
          if (lname.find('ouza') > 0):
            pass
          if (lname == possln):
            lnMatch  += 1

      for f in fnameList:
        possfn = self.CapName(f)
        for fname in fnaliasList:
          if (fname == possfn):
            fnMatch  += 1

      matchList.append((lnMatch,fnMatch))

      index += 1

    faeFoundCnt = 0
    faeIndex    = None
    index       = 0
    for fae in team.list:
      lnMatch,fnMatch = matchList[index]
      if (lnMatch > 0 and fnMatch > 0):
        faeFoundCnt += 1
        faeFound = True
        faeIndex = index
      index += 1

    if (faeIndex != None):
      #logging.info('Filename|' + filename)
      #logging.info('fae     |' + str(team.list[faeIndex].fullname))
      #logging.info('found   |' + str(faeFound))
      #logging.info('fndCnt  |' + str(faeFoundCnt))
      pass
    else:
      #logging.info('Filename|' + filename)
      #logging.info('found   |' + str(faeFound))
      #logging.info('fndCnt  |' + str(faeFoundCnt))
     pass

    if (faeFoundCnt > 1):
      logging.error('Multpile FAEs matched filename|' + filename)

    if (faeFound):
      fae = team.list[faeIndex]
    else:
      return

    #------------------------------------------------------------------
    # Try to figure out the date
    #------------------------------------------------------------------

    estWsDate = None
    estWeDate = None

    if (estweek):
      estWsDate = Calendar.GetWsDate(estweek)
      estWeDate = Calendar.GetWeDate(estweek)

    year = re.compile('2016',re.IGNORECASE)
    match = year.search(filename)
    if (match):
      yearStart = match.start()

      date = re.compile(r'^\d+-\d+-\d+')
      match = date.search(filename[yearStart:])
      sep = '-'
      if (not match):
        date = re.compile(r'^\d+_\d+_\d+')
        match = date.search(filename[yearStart:])
        sep = '_'
        if (match):
          date = filename[match.start()+yearStart:match.end()+yearStart]
          date = date.split(sep)
        else:
          date = None

      year = None
      mon  = None
      day  = None
      if (date):
        try:
          year = int(date[0])
          if (year < 2016 or year > 2024): year = None
        except TypeError:
          year = None
        try:
          mon  = int(date[1])
          if (mon < 1 or mon > 12): mon = None
        except TypeError:
          mon  = None
        try:
          day  = int(date[2])
          if (day < 1 or day > 31): day = None
        except TypeError:
          day  = None
      if (year and mon and day):
        date = datetime.date(year,mon,day)
        if (estWsDate and estWeDate):
          if (date >= estWsDate and date <= estWeDate):
            wsDate = estWsDate
            weDate = estWeDate
          else:
            wsDate = None
            weDate = None
        else:
          if (date in Calendar.wsDates):
            wsDate = date
            weDate = date + datetime.timedelta(days = 6)
          elif (date in Calendar.weDates):
            weDate = date
            wsDate = date - datetime.timedelta(days = 6)
          else:
            wsDate = None
            weDate = None

    # If all else fails just use the estimated dates
    if (not weDate and not wsDate):
      wsDate = estWsDate
      weDate = estWeDate

    self.fae      = fae
    self.fname    = str(fae.fname)
    self.lname    = str(fae.lname)
    self.fullname = str(fae.fname) + ' ' + str(fae.lname)
    self.filename = fullpath
    self.weDate   = weDate
    self.wsDate   = wsDate
    self.valid    = True

    return

  #--------------------------------------------------------------------
  def CapName(self,name):
    noncharRe = re.compile(r'\W+')
    match = noncharRe.search(name)
    if (match == None):
      return name.capitalize()
    else:
      if (len(match.regs) == 1):

        #text = '|'
        #for i in range(len(name)):
        #  c = name[i:i+1]
        #  o = str(ord(c)).rjust(3)
        #  text += c + '-' + o + '|'
        #logging.debug(text)

        sep = name[match.regs[0][0]:match.regs[0][1]]
        if (len(sep) == 1):
          return string.capwords(name,sep)
        else:
          logging.debug(name)
          logging.debug(match.regs)
          logging.debug(len(match.regs))
          logging.error('Unable to capitalize name')
          return name
      else:
        logging.debug(name)
        logging.debug(match.regs)
        logging.debug(len(match.regs))
        logging.error('Unable to capitalize name')
        return name

      #return string.capwords(name)
     
  #--------------------------------------------------------------------
  def __lt__(self,other): 
    if (str(self.fae.team) != str(other.fae.team)):
      if (str(self.fae.team) < str(other.fae.team)):
        return True
      else:
        return False
    elif (str(self.fae.loc) != str(other.fae.loc)):
      if (str(self.fae.loc) < str(other.fae.loc)):
        return True
      else:
        return False
    elif (str(self.fae.lname) != str(other.fae.lname)):
      if (str(self.fae.lname) < str(other.fae.lname)):
        return True
      else:
        return False
    elif (str(self.fae.fname) != str(other.fae.fname)):
      if (str(self.fae.fname) < str(other.fae.fname)):
        return True
      else:
        return False
    logging.error('SHOULD NOT BE HERE')
    return False

  #--------------------------------------------------------------------
  def __lt__(self,other): 
    return True
  def __le__(self,other): 
    return True
  def __gt__(self,other): 
    return True
  def __ge__(self,other): 
    return True
  def __eq__(self,other): 
    return True
  def __ne__(self,other): 
    return True

  def AddFAE(self,fae):
    self.fae = fae

  def IsValid(self):
    return (self.valid == True and self.fae != None)

  def Log(self):
    pass
    #logging.debug(str(self.wsDate) + ' ' + self.fname + ' ' + self.lname)

#-----------------------------------------------------------------------
class FlData:
  def __init__(self,root,team):
    self.weeks    = {}
    self.team  = team

    filelist = self.GetFiles(root)

    for file in filelist:

      dname = os.path.dirname(file)
      dname = dname.split('\\')
      dname = dname[-1]
      if (dname[:1].upper() == 'W'):
        estweek = dname[1:]
        try:
          estweek = int(estweek)
        except TypeError:
          estweek = None

      flFile = FlFile(file,team,estweek)
      if (flFile.IsValid()):
        self.AddFile(flFile)
      else:
        logging.error('Invalid File ' + file)

    self.Validate()

  #---------------------------------------------------------------------
  def AddFile(self,tsfile):
    date = tsfile.wsDate
    if (date not in self.weeks): 
      self.weeks[date] = {}
    name = tsfile.fullname
    if (name not in self.weeks[date]):
      self.weeks[date][name] = tsfile
    else:
      logging.error('Timesheet already exists for ' + str(date) + ' ' + name)

  #---------------------------------------------------------------------
  def Validate(self):
    for date in self.weeks:
      cnt = 0
      for name in self.team.dict:
        if (name not in self.weeks[date]):
          # Date is a Monday, so weDate should be a Friday
          wsDate = date.strftime('%Y-%m-%d')
          weDate = (date + datetime.timedelta(days=4)).strftime('%Y-%m-%d')
          sDate = self.team.dict[name].startDate
          tDate = self.team.dict[name].endDate
          if (wsDate >= sDate and weDate <= tDate):
            logging.error('Missing Timesheet for week starting ' + str(date) + ' ' + name)
        else:
          cnt += 1

  #---------------------------------------------------------------------
  def GetFiles(self,root):
    list = []
    self.Walk(root, list)
    return list

  #---------------------------------------------------------------------
  def Walk(self,rootdir, list):
    for curdir, subdirs, files in os.walk(rootdir):
      for file in files:

        master  = re.compile('master',re.IGNORECASE)
        msMatch = master.search(file)
        summary = re.compile('summary',re.IGNORECASE)
        ssMatch = summary.search(file)
        timesheet = re.compile('timesheet',re.IGNORECASE)
        tsMatch = timesheet.search(file)
        if (not ssMatch and not msMatch and tsMatch):
          fname = os.path.join(rootdir,file)
          list.append(fname)
      if (subdirs):
        for subdir in subdirs:
          dir = os.path.join(rootdir,subdir)
          self.Walk(dir, list)
      break

