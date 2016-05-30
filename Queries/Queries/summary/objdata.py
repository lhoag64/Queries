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
    self.regionList  = None
    self._calcRegionList(self.region)

  #--------------------------------------------------------------------
  def _calcTitleText(self,text,regionList,period):
    if (period == 'ALL'): period = 'YTD'
    title = text
    title += '\r'
    if (len(regionList) == 1):
       title += 'Region: '
    else:
       title += 'Regions: '
    title += ','.join(regionList)
    title += '\r'
    title += 'Period: ' + period

    return title

  #--------------------------------------------------------------------
  def _calcRegionList(self,region):

    if (type(region) is list):
      if ('ALL' in region or 'GLOBAL' in region):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = region
    else:
      if (region == 'ALL' or region == 'GLOBAL'):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = [region]

    self.regionList = regionList

    return regionList

