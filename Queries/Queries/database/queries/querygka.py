import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
#TODO GKT by Region
class QueryGka(Query):

  #--------------------------------------------------------------------
  def __init__(self,db):
    super().__init__(db)

  #--------------------------------------------------------------------
  def GetData(self,regionList,weekDict,**kwargs):
    super()._getWeeks(weekDict)
    minWeeks = self.minWeekCnt
    maxWeeks = self.maxWeekCnt

    data = self._getData(regionList,weekDict,maxWeeks,minWeeks)

    colComp = super()._calcRowMetrics(data['DATA'])
    rowComp = super()._calcColMetrics(data['DATA'])
    tblComp = super()._calcTblMetrics(data['DATA'])

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks):

    gkaDict = self._getGkaDict()
    gkaCnt  = len(gkaDict)

    data    = [[None for col in range(maxWeeks)] for row in range(gkaCnt)]
    rowHdr  = [[None for col in range(       1)] for row in range(gkaCnt)]
    colHdr  = [[None for col in range(maxWeeks)] for row in range(     1)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      gkaResult = self._queryGka(wcDate,weDate,regionList)
      othResult = self._queryOth(wcDate,weDate,regionList)

      nokSum    = 0.0
      aluSum    = 0.0
      nokAluSum = 0.0
      for item in gkaResult:
        if (item[0] in ['NOK','NSN','ALU','ASB']):
          nokAluSum += float(item[1])
          if (item[0] in ['NOK','NSN']):
            nokSum += float(item[1])
          if (item[0] in ['ALU','ASB']):
            aluSum += float(item[1])
        else:
          if (item[0] in gkaDict):
            data[gkaDict[item[0]][0]][colIdx] = float(item[1])
          else:
            logging.debug(item[0])

      data[gkaDict['NOK'    ][0]][colIdx] = float(nokSum)
      data[gkaDict['ALU'    ][0]][colIdx] = float(aluSum)
      data[gkaDict['NOK-ALU'][0]][colIdx] = float(nokAluSum)
      data[gkaDict['Others' ][0]][colIdx] = float(othResult[0][0])

      for rowIdx in range(gkaCnt):
        if (data[rowIdx][colIdx] == None):
          data[rowIdx][colIdx] = 0.0

    for colIdx in range(maxWeeks):
      colHdr[0][colIdx] = 'Week ' + str(weekDict['MAX'][colIdx][1])

    idx = 0
    for item in gkaDict:
      rowHdr[idx][0] = gkaDict[item][1]
      idx += 1

    result = {}
    result['DATA'] = data
    result['RHDR'] = rowHdr
    result['CHDR'] = colHdr
    result['ROWS'] = gkaCnt
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _queryGka(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT wbs.code,SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and (wbs.gl_tm_key_acct = 1)'
    sqltxt += '  GROUP BY wbs.gl_tm_key_acct_order,wbs.code'

    return super()._runQuery(sqlopt,sqltxt)

  def _queryOth(self,wcDate,weDate,regionList):

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT SUM(ts.hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '    and (wbs.gl_tm_key_acct = 0)'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getGkaDict(self):

    sqlopt  = []
    sqltxt  = 'SELECT wbs.code,wbs.desc,wbs.gl_tm_key_acct_order'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code'
    sqltxt += '  WHERE '
    sqltxt += '        (wbs.gl_tm_key_acct = 1)'
    sqltxt += '    and (wbs.gl_tm_key_acct_order < 99)'
    sqltxt += '  GROUP BY wbs.gl_tm_key_acct_order,wbs.code'

    dbResult = super()._runQuery(sqlopt,sqltxt)

    dbResult.insert(3,('NOK-ALU','Nokia/ALU Combined',3))
    dbResult.insert(4,('Others' ,'All Others',4))

    result = OrderedDict()
    for item in dbResult:
      result[item[0]] = (item[2],item[1])

    return result


