import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
KeyLocDict = { 'EMEA':'emea_key','AM':'am_key','GC':'gc_key','ROAPAC':'roapac_key'}
  
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
    14       :'Japan',                 \
    15       :'Korea',                 \
    16       :'India',                 \
    17       :'ROAPAC Other',          \
    'OTHER'  :'Other (outside region)' \
  }

#----------------------------------------------------------------------
class QueryActByLoc(Query):

  #--------------------------------------------------------------------
  def __init__(self,db):
    super().__init__(db)

  #--------------------------------------------------------------------
  def GetData(self,regionDict,weekDict,**kwargs):
    super()._getWeeks(weekDict)
    minWeeks = self.minWeekCnt
    maxWeeks = self.maxWeekCnt

    data = self._getData(regionDict,weekDict,maxWeeks,minWeeks,kwargs)

    colComp = super()._calcRowMetrics(data['DATA'])
    rowComp = super()._calcColMetrics(data['DATA'])
    tblComp = super()._calcTblMetrics(data['DATA'])

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionDict,weekDict,maxWeeks,minWeeks,kwargs):

    act = kwargs['act']['ACT']

    locDict = self._getLocDict(regionDict)
    locCnt  = len(locDict['GRP'])

    data   = [[None for col in range(maxWeeks)] for row in range(locCnt)]
    rowHdr = [[None for col in range(       1)] for row in range(locCnt)]
    colHdr = [[None for col in range(maxWeeks)] for row in range(     1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._query(wcDate,weDate,regionDict,act)

      if (len(dbResult) == 0):
        continue

      other = 0.0
      for item in dbResult:
        if (item[0] in locDict['GRP']):
          idx = locDict['GRP'][item[0]]
          data[idx][colIdx] = float(item[1])
        else:
          other += item[1]

      idx = locDict['GRP']['OTHER']
      data[idx][colIdx] = float(other)

      for rowIdx in range(locCnt):
        if (data[rowIdx][colIdx] == None):
          data[rowIdx][colIdx] = 0.0

    for colIdx in range(maxWeeks):
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
  def _query(self,wcDate,weDate,regionDict,act):

    sqlopt  = [wcDate,weDate,act]
    sqltxt  = 'SELECT loc.loc_group,SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_loc  AS loc ON (ts.work_loc = loc.loc)'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionDict,'ts.region')
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
  def _getLocDict(self,regionDict):

    result = {}
    result['KEY'   ] = OrderedDict()
    result['GRP'   ] = OrderedDict()
    result['OTHERS'] = OrderedDict()
    result['HDR'   ] = None

    grpDict = {}

    #logging.debug('---------------------------------------')
    for region in regionDict['LIST']:
      dbResult = self._queryRgnLoc(region)

      for item in dbResult:
        #text  = '|'
        #text += 'Code: '  + str(item[0]).rjust(3)  + '|'
        #text += 'Order: ' + str(item[1]).rjust(3)  + '|'
        #text += 'Group: ' + str(item[2]).rjust(3)  + '|'
        #text += 'Desc1: ' + str(item[3]).ljust(25) + '|'
        #text += 'Desc2: ' + str(item[4]).ljust(15) + '|'
        #text += 'Desc3: ' + str(item[5]).ljust(12) + '|'
        #text += 'Key  : ' + str(item[6]).rjust(1)  + '|'
        #logging.debug(text)
        if (item[6] == 1):
          result['KEY'][item[0]] = item[5]
        else:
          result['OTHERS'][item[0]] = item[5]
        if (item[2] not in grpDict):
          grpDict[item[2]] = NameLookup[item[2]]

      #logging.debug('---------------------------------------')

    idx = 0
    grpList = sorted(grpDict)
    for item in grpList:
      result['GRP'][item] = idx
      idx += 1
    result['GRP']['OTHER'] = idx

    hdrDict = OrderedDict()
    grpDict = {}

    for region in regionDict['LIST']:
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

