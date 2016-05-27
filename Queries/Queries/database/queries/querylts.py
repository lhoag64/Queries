import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
class QueryLts(Query):

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
    tblComp = super()._calcTblMetrics(data['DATA'])

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks,kwargs):

    ltsDict = self._getLtsDict()
    ltsCnt  = len(ltsDict)

    data   = [[None for col in range(maxWeeks)] for row in range(ltsCnt)]
    rowHdr = [[None for col in range(       1)] for row in range(ltsCnt)]
    colHdr = [[None for col in range(maxWeeks)] for row in range(     1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._query(wcDate,weDate,regionList)

      other = 0.0
      for item in dbResult:
        if (item[0] not in ltsDict):
          other += float(item[1])
        else:
          try:
            idx = ltsDict[item[0]]
          except KeyError:
            raise
          hrs = float(item[1])
          data[idx][colIdx] = float(hrs)

      data[ltsCnt-1][colIdx] = float(other)

      for rowIdx in range(ltsCnt):
        if (data[rowIdx][colIdx] == None):
          data[rowIdx][colIdx] = 0.0

    for colIdx in range(maxWeeks):
      colHdr[0][colIdx] = 'Week ' + str(weekDict['MAX'][colIdx][1])

    for (idx,item) in enumerate(ltsDict):
      rowHdr[idx][0] = item

    result = {}
    result['DATA'] = data
    result['RHDR'] = rowHdr
    result['CHDR'] = colHdr
    result['ROWS'] = ltsCnt
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _query(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT work_type,SUM(hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '  GROUP BY work_type'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getLtsDict(self):

    sqlopt  = []
    sqltxt  = 'SELECT key'
    sqltxt += '  FROM ts_lts'

    dbResult = super()._runQuery(sqlopt,sqltxt)

    idx    = 0
    result = OrderedDict()
    for item in dbResult:
      result[item[0]] = idx
      idx += 1
    result['Other (Not Specified)'] = idx

    return result


