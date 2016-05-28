import logging

#----------------------------------------------------------------------
class WbItem:
  def __init__(self,info):
    self.loc      = info[0]   # (0,0)
    self.wsName   = info[1]   # FAE YTD
    self.objType  = info[2]   # MATRIX
    self.region   = info[3]   # EMEA
    self.period   = info[4]   # ALL
    self.objName  = info[5]   # UTL-CF
    self.optName  = info[6]   # varies
    self.options  = info[7]   # varies
    self.objFunc  = self._getFuncName()
    self.fullName = self._getFullName()
    self.data     = None
    self.view     = None
    self.hgt      = None
    self.wid      = None
    self.ws       = None

  #--------------------------------------------------------------------
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

  #--------------------------------------------------------------------
  def CreateMatrixData(self,func,item):
    data = func(item)

    self.data = data.tbl
    self.hgt  = data.tbl['ROWS']
    self.wid  = data.tbl['COLS']

  #--------------------------------------------------------------------
  def CreateSummaryData(self,func,itemDict,nameDict):
    data = func(itemDict,nameDict)

    self.data = data.tbl
    self.hgt  = data.tbl['ROWS']
    self.wid  = data.tbl['COLS']

  #--------------------------------------------------------------------
  def CreateChartData(self,func,itemDict,nameDict):
    data = func(itemDict,nameDict)

    self.data = data.tbl
    self.hgt  = data.tbl['ROWS']
    self.wid  = data.tbl['COLS']

  #--------------------------------------------------------------------
  def AddWsObj(self,ws,wsObj):
    self.ws    = ws
    self.wsObj = wsObj
  
  #--------------------------------------------------------------------
  def _getFuncName(self):
    objType = self._cleanName(self.objType)
    objName = self._cleanName(self.objName)
    return objType + '_' + objName

  #--------------------------------------------------------------------
  def _getFullName(self):
    wsName  = self._cleanName(self.wsName)
    objType = self._cleanName(self.objType)
    region  = self._cleanName(self.region)
    objName = self._cleanName(self.objName)
    optName = self._cleanName(self.optName)
    period  = self._cleanName(self.period)
    fullname = wsName + '.' + objType + '.' + region + '.' + period + '.' + objName
    if (optName != None):
      fullname += '.' + optName
    return fullname
