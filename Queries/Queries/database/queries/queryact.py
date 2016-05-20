import logging
from   collections            import OrderedDict
from   database.queries.query import Query

#----------------------------------------------------------------------
class QueryAct(Query):

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
    tblComp = super()._calcTblMetrics(data)

    return {'TBL-DATA':data,'ROW-COMP':rowComp,'COL-COMP':colComp,'TBL-COMP':tblComp}

  #--------------------------------------------------------------------
  def _getData(self,regionList,weekDict,maxWeeks,minWeeks):

    actList = self._getActList()
    actCnt  = len(actList) + 1

    data = [[None for col in range(maxWeeks)] for row in range(actCnt)]
    for colIdx in range(minWeeks):

      wcDate = weekDict['MIN'][colIdx][0]
      weDate = super()._getWeDate(wcDate)

      dbResult = self._query(wcDate,weDate,regionList)

      other = 0.0
      for item in dbResult:
        if (item[0] == None or item[0] == ''):
          other += float(item[1])
        else:
          act = int(item[0])
          idx = act - 10
          hrs = float(item[1])
          data[idx][colIdx] = hrs

      data[actCnt-1][colIdx] = other

      for rowIdx in range(actCnt):
        if (data[rowIdx][colIdx] == None):
          data[rowIdx][colIdx] = 0.0

      #for rowIdx in range(actCnt):
      #  text  = ''
      #  for colIdx in range(maxWeeks):
      #    text += ''
      #  logging.debug(text)

    result = {}
    result['DATA'] = data
    result['ROWS'] = actCnt
    result['COLS'] = maxWeeks

    return result

  #--------------------------------------------------------------------
  def _query(self,wcDate,weDate,regionList):

    # Detailed query
    #sqltxt  = 'SELECT fname,lname,region,activity,wbs_code,entry_date'

    sqlopt  = [wcDate,weDate]
    sqltxt  = 'SELECT activity,SUM(hours)'
    sqltxt += '  FROM ts_entry AS ts'
    sqltxt += '  WHERE ' + super()._getRegionWhereClause(regionList,'ts.region')
    sqltxt += '    and (ts.entry_date >= ? and ts.entry_date <= ?)'
    sqltxt += '  GROUP BY activity'

    return super()._runQuery(sqlopt,sqltxt)

  #--------------------------------------------------------------------
  def _getActList(self):

    sqlopt  = []
    sqltxt  = 'SELECT act'
    sqltxt += '  FROM ts_act'

    dbResult = super()._runQuery(sqlopt,sqltxt)

    result = []
    for item in dbResult:
      result.append(item[0])

    return result

#----------------------------------------------------------------------
class QueryActList(Query):

  #--------------------------------------------------------------------
  def __init__(self,db):
    super().__init__(db)

  #--------------------------------------------------------------------
  def GetData(self,**kwargs):

    sqlopt  = []
    sqltxt  = 'SELECT act,desc'
    sqltxt += '  FROM ts_act'

    dbResult = super()._runQuery(sqlopt,sqltxt)

    result = OrderedDict()
    for item in dbResult:
      result[item[0]] = item[1]

    return result


