import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
KeyLocDict = { 'EMEA':'emea_key','AM':'am_key','GC':'gc_key'}
  
NameLookup =                           \
  {                                    \
     1       :'UK',                    \
     2       :'Sweden',                \
     3       :'Finland',               \
     4       :'France',                \
     5       :'Germany',               \
     6       :'EMEA Other',            \
    10       :'US-East',               \
    11       :'US-West',               \
    12       :'CA-East',               \
    13       :'AM Other',              \
     9       :'Greater China',         \
    'OTHER'  :'Other (outside region)' \
  }

#----------------------------------------------------------------------
class QueryActByLoc(Query):

  #--------------------------------------------------------------------
  def __init__(self,db):
    super().__init__(db)

  #--------------------------------------------------------------------
  def GetData(self,regionList,weekDict,**kwargs):
    super()._getWeeks(weekDict)
    minWeeks = self.minWeekCnt
    maxWeeks = self.maxWeekCnt

    data = self._getData(regionList,weekDict,maxWeeks,minWeeks,kwargs)

    colComp = super()._calcRowMetrics(data['DATA'])
    rowComp = super()._calcColMetrics(data['DATA'])
    tblComp = super()._calcTblMetrics(data)

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks,kwargs):

    act = kwargs['act']['ACT']

    locDict = self._getLocDict(regionList)
    locCnt  = len(locDict['GRP'])

    data   = [[None for col in range(maxWeeks)] for row in range(locCnt)]
    rowHdr = [[None for col in range(       1)] for row in range(locCnt)]
    colHdr = [[None for col in range(maxWeeks)] for row in range(     1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._query(wcDate,weDate,regionList,act)

      other = 0.0
      for item in dbResult:
        if (item[0] in locDict['GRP']):
          idx = locDict['GRP'][item[0]]
          data[idx][colIdx] = item[1]
        else:
          other += item[1]

      idx = locDict['GRP']['OTHER']
      data[idx][colIdx] = other

      for rowIdx in range(locCnt):
        if (data[rowIdx][colIdx] == None):
          data[rowIdx][colIdx] = 0.0

      colHdr[0][colIdx] = 'Week ' + str(weekDict['MAX'][colIdx][1])

    for (idx,item) in enumerate(locDict['HDR']):
      rowHdr[idx][0] = locDict['HDR'][item]

    result = {}
    result['DATA'] = data
    result['RHDR'] = rowHdr
    result['CHDR'] = colHdr
    result['ROWS'] = locCnt
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _query(self,wcDate,weDate,regionList,act):

    sqlopt  = [wcDate,weDate,act]
    sqltxt  = 'SELECT loc.loc_group,SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and ts.activity= ?'
    sqltxt += '  GROUP BY loc.loc_group'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _queryRgnLoc(self,region):

    sqlopt  = []
    sqltxt  = 'SELECT loc,loc_order,loc_group,desc,rgn_desc,rgn_loc,' + KeyLocDict[region]
    sqltxt += '  FROM ts_loc'
    sqltxt += '  WHERE region = \'' + region + '\''
    sqltxt += '  ORDER BY loc_group,loc_order'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getLocDict(self,regionList):

    result = {}
    result['KEY'   ] = OrderedDict()
    result['GRP'   ] = OrderedDict()
    result['OTHERS'] = OrderedDict()
    result['HDR'   ] = None

    grpDict = {}

    logging.debug('---------------------------------------')
    for region in regionList:
      dbResult = self._queryRgnLoc(region)

      for item in dbResult:
        text  = '|'
        text += 'Code: '  + str(item[0]).rjust(3)  + '|'
        text += 'Order: ' + str(item[1]).rjust(3)  + '|'
        text += 'Group: ' + str(item[2]).rjust(3)  + '|'
        text += 'Desc1: ' + str(item[3]).ljust(25) + '|'
        text += 'Desc2: ' + str(item[4]).ljust(15) + '|'
        text += 'Desc3: ' + str(item[5]).ljust(12) + '|'
        text += 'Key  : ' + str(item[6]).rjust(1)  + '|'
        logging.debug(text)
        if (item[6] == 1):
          result['KEY'][item[0]] = item[5]
        else:
          result['OTHERS'][item[0]] = item[5]
        if (item[2] not in grpDict):
          grpDict[item[2]] = NameLookup[item[2]]

      logging.debug('---------------------------------------')

    idx = 0
    grpList = sorted(grpDict)
    for item in grpList:
      result['GRP'][item] = idx
      idx += 1
    result['GRP']['OTHER'] = idx

    hdrDict = OrderedDict()
    grpDict = {}

    for region in regionList:
      dbResult = self._queryRgnLoc(region)
      for item in dbResult:
        if (item[2] not in grpDict):
          grpDict[item[2]] = NameLookup[item[2]]

    grpList = sorted(grpDict)
    for item in grpList:
      hdrDict[item] = grpDict[item]
    hdrDict['OTHER'] = NameLookup['OTHER']

    result['HDR'] = hdrDict

    return result

#----------------------------------------------------------------------
#class QueryActByLocList(Query):
#
#  #--------------------------------------------------------------------
#  def __init__(self,db):
#    super().__init__(db)
#
#  #--------------------------------------------------------------------
#  def GetData(self,**kwargs):
#
#    regionList = kwargs['rgnList']
#
#    result  = OrderedDict()
#    grpDict = {}
#
#    for region in regionList:
#      dbResult = self._queryRgnLoc(region)
#      for item in dbResult:
#        if (item[2] not in grpDict):
#          grpDict[item[2]] = NameLookup[item[2]]
#
#    grpList = sorted(grpDict)
#    for item in grpList:
#      result[item] = grpDict[item]
#    result['OTHER'] = NameLookup['OTHER']
#
#    return result
#
#  #--------------------------------------------------------------------
#  def _queryRgnLoc(self,region):
#
#    sqlopt  = []
#    sqltxt  = 'SELECT loc,loc_order,loc_group,desc,rgn_desc,rgn_loc,' + KeyLocDict[region]
#    sqltxt += '  FROM ts_loc'
#    sqltxt += '  WHERE region = \'' + region + '\''
#    sqltxt += '  ORDER BY loc_group,loc_order'
#
#    return super()._runQuery(sqlopt,sqltxt)


##----------------------------------------------------------------------
#class QueryActList(Query):
#
#  #--------------------------------------------------------------------
#  def __init__(self,db):
#    super().__init__(db)
#
#  #--------------------------------------------------------------------
#  def GetData(self,**kwargs):
#
#    sqlopt  = []
#    sqltxt  = 'SELECT act,desc'
#    sqltxt += '  FROM ts_act'
#
#    dbResult = super()._runQuery(sqlopt,sqltxt)
#
#    result = OrderedDict()
#    for item in dbResult:
#      result[item[0]] = item[1]
#
#    return result




##----------------------------------------------------------------------
#def consolidate(regionList,weekCnt,hrsDict):
#  hoursDict = {}
#  grpDict = {}
#  for region in ['EMEA','GC','AM','APAC']:
#    if (region in regionList):
#      for idx in hrsDict[region]['LOCDICT']:
#        locTup = hrsDict[region]['LOCDICT'][idx]
#        key  = locTup[6]
#        grp  = locTup[2]
#        name = locTup[5]
#        if (key == 0):
#          name = 'Other (' + region + ')'
#        else:
#          name = NameLookup[name]
#        grpDict[grp] = name
#  grpList = sorted(grpDict.items())
#
#  hoursDict['GRPDICT'] = grpDict
#  hoursDict['GRPLIST'] = grpList
#  hoursDict['HRSLIST'] = []
#
#  weekList = []
#  for i in range(weekCnt):
#    hourData = {}
#    for region in ['EMEA','GC','AM','APAC']:
#      if (region in hrsDict):
#        weekData = hrsDict[region]['HOURS']
#        week = weekData[i]
#        for item in week:
#          hourData[item[0]] = item[1]
#
#    hourList = []
#    for item in hoursDict['GRPLIST']:
#      if (item[0] in hourData):
#        hourList.append((item[0],item[1],float(hourData[item[0]])))
#      else:
#        hourList.append((item[0],item[1],0.0))
#
#    weekList.append(hourList)
#
#  hoursDict['HRSLIST'] = weekList
#  return hoursDict

##----------------------------------------------------------------------
#def GetActByLocSum(db,regionList,weekDict,act):
#
#  c = db.cursor()
#
#  minWeekCnt = len(weekDict['MIN'])
#  maxWeekCnt = len(weekDict['MAX'])
#  dltWeekCnt = maxWeekCnt - minWeekCnt
#
#  hrsDict = {}
#
#  sqlopt  = [act]
#  sqltxt  = 'SELECT act,desc FROM ts_act WHERE act = ?'
#  c.execute(sqltxt,tuple(sqlopt))
#  actList = c.fetchall()
#  title = actList[0][1] + ' - ' + str(actList[0][0])
#
#  for region in regionList:
#    if (region not in hrsDict):
#      sqlopt  = []
#      sqltxt  = 'SELECT loc,loc_order,loc_group,desc,rgn_desc,rgn_loc,' + KeyLocDict[region]
#      sqltxt += '  FROM ts_loc'
#      sqltxt += '  WHERE region = \'' + region + '\''
#      sqltxt += '  ORDER BY loc_group,loc_order'
#
#      c.execute(sqltxt,tuple(sqlopt))
#      locList = c.fetchall()
#
#      grpDict = {}
#      for item in locList:
#        grpDict[item[2]] = item
#
#      hrsDict[region] = {'HOURS':[],'LOCLIST':locList,'LOCDICT':grpDict}
#
#  for i in range(minWeekCnt):
#
#    wcDate = weekDict['MIN'][i][0]
#    weDate = GetWeDate(wcDate)
#
#    for region in regionList:
#
#      sqlopt  = [wcDate,weDate,act]
#      sqltxt  = 'SELECT loc.loc_group,SUM(ts.hours)'
#      sqltxt += '  FROM ts_entry AS ts'
#      sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
#      sqltxt += '  WHERE ts.region = \'' + region + '\''
#      sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
#      sqltxt += '    and ts.activity= ?'
#      #sqltxt += '    and ' + KeyLocDict[region] + ' = 1'
#      sqltxt += '  GROUP BY loc.loc_group'
#
#      c.execute(sqltxt,tuple(sqlopt))
#      dbResult = c.fetchall()
#
#      hrsDict[region]['HOURS'].append(dbResult)
#
#  hoursDict = consolidate(regionList,minWeekCnt,hrsDict)
#
#  if (dltWeekCnt != 0):
#    for i in range(dltWeekCnt):
#      hoursDict['HRSLIST'].append(None)
#
#  hoursDict['TITLE'] = title
#
#  return hoursDict

