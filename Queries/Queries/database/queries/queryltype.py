import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
class QueryLType(Query):

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

    ltDict = self._getLtDict()
    ltCnt  = len(ltDict)

    data   = [[None for col in range(maxWeeks)] for row in range(ltCnt)]
    rowHdr = [[None for col in range(       1)] for row in range(ltCnt)]
    colHdr = [[None for col in range(maxWeeks)] for row in range(     1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._query(wcDate,weDate,regionList)

      other = 0.0
      for item in dbResult:
        if (item[0] not in ltDict):
          other += float(item[1])
        else:
          try:
            idx = ltDict[item[0]][0]
          except KeyError:
            raise
          hrs = float(item[1])
          data[idx][colIdx] = hrs

      data[ltCnt-1][colIdx] = other

      for rowIdx in range(ltCnt):
        if (data[rowIdx][colIdx] == None):
          data[rowIdx][colIdx] = 0.0

      colHdr[0][colIdx] = 'Week ' + str(weekDict['MAX'][colIdx][1])

    for (idx,item) in enumerate(ltDict):
      rowHdr[idx][0] = ltDict[item][1]

    result = {}
    result['DATA'] = data
    result['RHDR'] = rowHdr
    result['CHDR'] = colHdr
    result['ROWS'] = ltCnt
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _query(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate,wcDate,weDate]
    sqltxt  = 'SELECT fae.lbr_type,sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)'
    sqltxt += '  INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'
    sqltxt += '  GROUP BY fae.lbr_type'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getLtDict(self):

    result = OrderedDict()
    result['P'] = (0,'Internal Hours')
    result['C'] = (1,'Contracted Hours')


    return result

