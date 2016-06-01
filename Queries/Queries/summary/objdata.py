import logging
from   collections import OrderedDict

#----------------------------------------------------------------------
class ObjData:

  #--------------------------------------------------------------------
  def __init__(self,item):

    self.item        = item
    self.region      = item.region
    self.objType     = item.objType  # MATRIX
    self.objName     = item.objName  # UTL-CF
    self.period      = item.period
    self.regionDict  = None
    self._calcregionDict(self.region)

  #--------------------------------------------------------------------
  def _calcTitleText(self,text,regionDict,period):
    if (period == 'ALL'): period = 'YTD'
    title = text
    title += '\r'
    if (len(regionDict['LIST']) == 1):
       title += 'Region: '
    else:
       title += 'Regions: '
    title += ','.join(regionDict['LIST'])
    title += '\r'
    title += 'Period: ' + period

    return title

  #--------------------------------------------------------------------
  def _calcregionDict(self,region):

    regionDict = {}
    regionDict['TYPE'] = None
    regionDict['LIST'] = []

    if (type(region) is list):
      if ('ALL' in region or 'GLOBAL' in region):
        regionDict['TYPE'] = 'GLOBAL'
        regionDict['LIST'] = ['EMEA','AM','GC','ROAPAC']
      else:
        if (len(region) > 1):
          regionDict['TYPE'] = 'GLOBAL'
          regionDict['LIST'] = region
        else:
          regionDict['TYPE'] = 'LOCAL'
          regionDict['LIST'] = [region]
    else:
      if (region == 'ALL' or region == 'GLOBAL'):
        regionDict['TYPE'] = 'GLOBAL'
        regionDict['LIST'] = ['EMEA','AM','GC','ROAPAC']
      else:
        regionDict['TYPE'] = 'LOCAL'
        regionDict['LIST'] = [region]

    self.regionDict = regionDict

    return regionDict

