import logging
from   database.queries.query import Query

#----------------------------------------------------------------------
class QueryUtl(Query):

  #--------------------------------------------------------------------
  def __init__(self,db):
    super().__init__(db)
 
    self._funcDict =              \
      {                           \
        'UTL-CF': self._queryCf,  \
        'UTL-PS': self._queryPs,  \
        'UTL-DT': self._queryDt,  \
        'UTL-LS': self._queryLs,  \
      }

  #--------------------------------------------------------------------
  def GetData(self,regionList,weekDict,**kwargs):
    super()._getWeeks(weekDict)
    minWeeks = self.minWeekCnt
    maxWeeks = self.maxWeekCnt

    data = self._getData(regionList,weekDict,maxWeeks,minWeeks,kwargs)

    colComp = super()._calcRowMetrics(data['DATA'])
    rowComp = super()._calcColMetrics(data['DATA'])
    tblComp = super()._calcTblMetrics(data)

    cols = data['COLS']
    utl  = [None for col in range(maxWeeks)]
    for colIdx in range(cols):
      tgt = data['DATA'][0][colIdx]
      tot = data['DATA'][1][colIdx]
      if (tgt != None and tot != None):
        utl[colIdx] = tgt/tot * 100.0

    rowComp['UTL'] = utl
    rowComp['DATA'].insert(0,utl)
    rowComp['ROWS'] += 1

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks,kwargs):

    queryType = kwargs['qtype']

    data = [[None for col in range(maxWeeks)] for row in range(2)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      tgtResult = self._funcDict[queryType](wcDate,weDate,regionList)
      totResult = self._queryTotal(wcDate,weDate,regionList)

      tgt = tgtResult[0][0]
      tot = totResult[0][0]
      if (tgt == None): tgt = 0.0
      if (tot == None): tot = 0.0
      data[0][colIdx] = float(tgt)
      data[1][colIdx] = float(tot)

    result = {}
    result['DATA'] = data
    result['ROWS'] = 2
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _queryTotal(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _queryCf(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_act AS act ON ts.activity = act.act'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and act.billable = 1'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _queryPs(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_act AS act ON ts.activity = act.act'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and act.pre_sales = 1'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _queryDt(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and wbs.downtime = 1'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _queryLs(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT sum(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and wbs.leave = 1'

    return super()._runQuery(sqlopt,sqltxt)

