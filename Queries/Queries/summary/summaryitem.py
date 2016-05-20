import logging

#----------------------------------------------------------------------
class SummaryItem:
  def __init__(self,info):
    self.loc      = info[0]   # (0,0)
    self.wsName   = info[1]   # FAE YTD
    self.rptType  = info[2]   # MATRIX
    self.region   = info[3]   # EMEA
    self.period   = info[4]   # ALL
    self.rptName  = info[5]   # UTL-CF
    self.optName  = info[6]   # varies
    self.options  = info[7]   # varies
    self.rptFunc  = self._getFuncName()
    self.fullName = self._getFullName()
    self.data     = None
    self.wsRpt    = None
    self.hgt      = None
    self.wid      = None

  def _cleanName(self,name):
    if (name != None):
      text = ''
      for i in name:
        if (i in [' ','-','\n','\r','\t']):
          ch = '_'
        else:
          ch = i
        text += ch
      return text
    else:
      return None

  def AddData(self,data):
    self.data = data.tbl
    self.hgt  = data.tbl['ROWS']
    self.wid  = data.tbl['COLS']

  def AddWsRpt(self,wsRpt):
    self.wsRpt = wsRpt
  
  def _getFuncName(self):
    rptType = self._cleanName(self.rptType)
    rptName = self._cleanName(self.rptName)
    return rptType + '_' + rptName

  def _getFullName(self):
    wsName  = self._cleanName(self.wsName)
    rptType = self._cleanName(self.rptType)
    region  = self._cleanName(self.region)
    rptName = self._cleanName(self.rptName)
    optName = self._cleanName(self.optName)
    period  = self._cleanName(self.period)
    fullname = wsName + '.' + rptType + '.' + region + '.' + period + '.' + rptName
    if (optName != None):
      fullname += '.' + optName
    return fullname
