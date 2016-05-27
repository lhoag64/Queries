import logging
from   collections            import OrderedDict
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
        'UTL-OT': self._queryOt,  \
      }

  #--------------------------------------------------------------------
  def GetData(self,regionList,weekDict,**kwargs):
    super()._getWeeks(weekDict)
    minWeeks = self.minWeekCnt
    maxWeeks = self.maxWeekCnt

    queryType = kwargs['qtype']

    data = self._getData(regionList,weekDict,maxWeeks,minWeeks,kwargs)

    colComp = super()._calcRowMetrics(data['DATA'])
    rowComp = super()._calcColMetrics(data['DATA'])
    tblComp = super()._calcTblMetrics(data['DATA'])

    cols = data['COLS']
    utl  = [None for col in range(maxWeeks)]
    for colIdx in range(cols):
      tgt = data['DATA'][0][colIdx]
      tot = data['DATA'][1][colIdx]
      if (tgt != None and tot != None):
        utl[colIdx] = tgt/tot * 100.0

    rowComp['DATA'].insert(0,utl)
    rowComp['ROWS'] += 1
    if (queryType in ['UTL-CF','UTL-PS','UTL-DT','UTL-LS']):
      rowComp['RHDR'].insert(0,['Utilisation as a %'])
    elif (queryType == 'UTL-OT'):
      rowComp['RHDR'].insert(0,['Additional Hours as a %'])
    else:
      logging.critical('Invalidat UTL query type: ' + queryType)
      raise

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks,kwargs):

    queryType = kwargs['qtype']

    data   = [[None for col in range(maxWeeks)] for row in range(2)]
    rowHdr = [[None for col in range(       1)] for row in range(2)]
    colHdr = [[None for col in range(maxWeeks)] for row in range(1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      tgtResult = self._funcDict[queryType](wcDate,weDate,regionList)
      totResult = self._queryTotal(wcDate,weDate,regionList)

      tgt = tgtResult[0][0]
      tot = totResult[0][0]
      if (tgt == None): tgt = 0.0
      if (tot == None): tot = 0.0

      if (queryType in ['UTL-CF','UTL-PS','UTL-DT','UTL-LS']):
        data[0][colIdx] = float(tgt)
        data[1][colIdx] = float(tot)
      elif (queryType == 'UTL-OT'):
        ot = tot - tgt
        if (ot < 0.0):
          ot = 0.0
        data[0][colIdx] = float(ot)
        data[1][colIdx] = float(tgt)
      else:
        logging.critical('Invalidat UTL query type: ' + queryType)
        raise

    for colIdx in range(maxWeeks):
      colHdr[0][colIdx] = 'Week ' + str(weekDict['MAX'][colIdx][1])

    if (queryType in ['UTL-CF','UTL-PS','UTL-DT','UTL-LS']):
      rowHdr[0][0] = 'For'
      rowHdr[1][0] = 'Total Time'
    elif (queryType == 'UTL-OT'):
      rowHdr[0][0] = 'Additional'
      rowHdr[1][0] = 'Contracted'
    else:
      logging.critical('Invalidat UTL query type: ' + queryType)
      raise

    result = {}
    result['DATA'] = data
    result['RHDR'] = rowHdr
    result['CHDR'] = colHdr
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
  #--------------------------------------------------------------------
  def _queryOt(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT SUM(fae.norm_hours)'
    sqltxt += '  FROM fae_team AS fae'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'fae.region')
    sqltxt += '    and (fae.start_date <= ? and fae.end_date >= ?)'

    return super()._runQuery(sqlopt,sqltxt)

