import logging

#----------------------------------------------------------------------
def GetRegionWhereClause(regionList,regionName='region'):
  where = ''
  for region in regionList:
    where += '(' + regionName + ' = \'' + region + '\') or '
  where = where[0:-4]
  return '(' + where + ')'

