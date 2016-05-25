import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
class QueryFae(Query):

  #--------------------------------------------------------------------
  def __init__(self,db):
    super().__init__(db)
 
    self._funcDict =                \
      {                             \
        'FAE-AWH': self._queryAwh,  \
      }

  #--------------------------------------------------------------------
  def GetData(self,regionList,weekDict,**kwargs):
    super()._getWeeks(weekDict)
    minWeeks = self.minWeekCnt
    maxWeeks = self.maxWeekCnt

    wdResults = self._getWd(regionList,weekDict,maxWeeks,minWeeks)
    hcResults = self._getHc(regionList,weekDict,maxWeeks,minWeeks)

    data = self._getData(regionList,weekDict,maxWeeks,minWeeks,kwargs)

    colComp = super()._calcRowMetrics(data['DATA'])
    rowComp = super()._calcColMetrics(data['DATA'])
    tblComp = super()._calcTblMetrics(data)

    for item in hcResults['DATA']:
      rowComp['DATA'].append(item)
    for item in hcResults['RHDR']:
      rowComp['RHDR'].append(item)
    rowComp['ROWS'] += hcResults['ROWS']

    for item in wdResults['DATA']:
      rowComp['DATA'].append(item)
    for item in wdResults['RHDR']:
      rowComp['RHDR'].append(item)
    rowComp['ROWS'] += wdResults['ROWS']

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks,kwargs):

    queryType = kwargs['qtype']

    dbResult = self._queryFae(regionList)
    faeCnt  = len(dbResult)
    faeList = []
    for fae in dbResult:
      faeList.append((fae[0],fae[1]))

    data   = [[None for col in range(maxWeeks)] for row in range(faeCnt)]
    rowHdr = [[None for col in range(       1)] for row in range(faeCnt)]
    colHdr = [[None for col in range(maxWeeks)] for row in range(     1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._funcDict[queryType](wcDate,weDate,regionList)
      dbDict = {}
      for item in dbResult:
        dbDict[(item[0],item[1])] = item[2]

      for rowIdx in range(faeCnt):
        fae = faeList[rowIdx]
        if (fae in dbDict):
          data[rowIdx][colIdx] = dbDict[fae]

      colHdr[0][colIdx] = 'Week ' + str(weekDict['MAX'][colIdx][1])

    for rowIdx in range(faeCnt):
      fae = faeList[rowIdx]
      rowHdr[rowIdx][0]    = fae[0] + ' ' + fae[1]

    result = {}
    result['DATA'] = data
    result['RHDR'] = rowHdr
    result['CHDR'] = colHdr
    result['ROWS'] = faeCnt
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _queryFae(self,regionList):

    sqlopt = []
    sqltxt  = 'SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type,start_date,end_date,region'
    sqltxt += '  FROM fae_team AS fae'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'fae.region')
    sqltxt += '  ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getWd(self,regionList,weekDict,maxWeeks,minWeeks):

    wdSelectText = ''
    wdList       = []
    wdCnt        = 0
    for region in regionList:
      if (region == 'EMEA'):
        wdSelectText += 'uk_days,se_days,fi_days,fr_days,de_days'
        wdList.append('UK Days')
        wdList.append('SE Days')
        wdList.append('FI Days')
        wdList.append('FR Days')
        wdList.append('DE Days')
        wdCnt += 5
      elif (region == 'AM'):
        wdSelectText += 'am_days'
        wdList.append('AM Days')
        wdCnt += 1
      elif (region == 'GC'):
        wdSelectText += 'gc_days'
        wdList.append('GC Days')
        wdCnt += 1
      else:
        raise
      wdSelectText += ','
    wdSelectText = wdSelectText[:-1]

    data = [[None for col in range(maxWeeks)] for row in range(wdCnt)]
    text = [[None for col in range(1)       ] for row in range(wdCnt)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._queryWd(wcDate,weDate,wdSelectText)

      rowIdx = 0
      for item in wdList:
        data[rowIdx][colIdx] = dbResult[0][rowIdx]
        rowIdx += 1

    rowIdx = 0
    for item in wdList:
      text[rowIdx][0] = item
      rowIdx += 1

    result = OrderedDict()
    result['DATA'] = data
    result['RHDR'] = text
    result['ROWS'] = wdCnt     
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _queryWd(self,wcDate,weDate,selectText):

    sqlopt  = [wcDate]
    sqltxt  = 'SELECT ' + selectText
    sqltxt += '  FROM weeks'
    sqltxt += '  WHERE wc_date == ?'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getHc(self,regionList,weekDict,maxWeeks,minWeeks):

    rgnList = []
    hcList  = []
    hcCnt   = 0
    for region in regionList:
      if (region == 'EMEA'):
        rgnList.append(['EMEA'])
        hcList.append('EMEA Headcount')
        hcCnt += 1
      elif (region == 'AM'):
        rgnList.append(['AM'])
        hcList.append('AM Headcount')
        hcCnt += 1
      elif (region == 'GC'):
        rgnList.append(['GC'])
        hcList.append('GC Headcount')
        hcCnt += 1
      else:
        raise
    if (len(regionList) > 1):
        rgnList.append(regionList)
        hcList.append('Total Headcount')
        hcCnt += 1

    data     = [[None for col in range(maxWeeks)] for row in range(hcCnt)]
    text     = [[None for col in range(1)       ] for row in range(hcCnt)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      rgnIdx = 0
      for item in rgnList:
        data[rgnIdx][colIdx] = self._queryHc(wcDate,weDate,rgnList[rgnIdx])
        rgnIdx += 1

    rowIdx = 0
    for item in hcList:
      text[rowIdx][0] = item
      rowIdx += 1

    result = OrderedDict()
    result['DATA'] = data
    result['RHDR'] = text
    result['ROWS'] = hcCnt     
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _queryHc(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT fae.fname,fae.lname,fae.start_date,fae.end_date'
    sqltxt += '  FROM fae_team AS fae'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'fae.region')
    sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'
    sqltxt += '  ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'

    return len(super()._runQuery(sqlopt,sqltxt))

  #--------------------------------------------------------------------
  def _queryAwh(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT ts.fname,ts.lname,sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
    sqltxt += '  INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0'
    sqltxt += '  GROUP BY fae.fname,fae.lname'
    sqltxt += '  ORDER BY fae.region,fae.prd_team,fae.lname,fae.fname'

    return super()._runQuery(sqlopt,sqltxt)

#----------------------------------------------------------------------
#class QueryFaeList(Query):
#
#  #--------------------------------------------------------------------
#  def __init__(self,db):
#    super().__init__(db)
#
#  #--------------------------------------------------------------------
#  def GetData(self,**kwargs):
#
##    sqlopt  = []
##    sqltxt  = 'SELECT act,desc'
##    sqltxt += '  FROM ts_act'
##
##    dbResult = super()._runQuery(sqlopt,sqltxt)
#
#    result = OrderedDict()
##    for item in dbResult:
##      result[item[0]] = item[1]
#
#    return result


