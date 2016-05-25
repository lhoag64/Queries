import logging
import datetime
import sqlite3

#----------------------------------------------------------------------
class Query:

  compList = ['Avg','Sum','Cnt']

  #--------------------------------------------------------------------
  def __init__(self,db):
    self.c = db.cursor()
 
  #--------------------------------------------------------------------
  def _getWeeks(self,weekDict):
    self.minWeekCnt = len(weekDict['MIN'])
    self.maxWeekCnt = len(weekDict['MAX'])
    self.dltWeekCnt = self.maxWeekCnt - self.minWeekCnt

  #--------------------------------------------------------------------
  def _getWeDate(self,wcDate):
    stxt = wcDate.split('-')
    wcDate = datetime.date(int(stxt[0]),int(stxt[1]),int(stxt[2]))
    weDate = wcDate + datetime.timedelta(days=6)
    weDate = weDate.strftime('%Y-%m-%d')
    return weDate

  #--------------------------------------------------------------------
  def _getRegionWhereClause(self,regionList,field='region'):
    where = ''
    for region in regionList:
      where += '(' + field + ' = \'' + region + '\') or '
    where = where[0:-4]
    return '(' + where + ')'

  #--------------------------------------------------------------------
  def _runQuery(self,sqlopt,sqltxt):

    self.c.execute(sqltxt,tuple(sqlopt))
    result = self.c.fetchall()
    return result

  #--------------------------------------------------------------------
  def _calcRowMetrics(self,data):
    rows = len(data)
    cols = len(data[0])

    sumList = [None for row in range(rows)]
    avgList = [None for row in range(rows)]
    cntList = [None for row in range(rows)]
    for rowIdx in range(rows):
      sum     = 0.0
      avg     = 0.0
      cnt     =   0
      noneCnt =   0
      for colIdx in range(cols):
        if (data[rowIdx][colIdx] != None):
          sum += float(data[rowIdx][colIdx])
          cnt += 1
        else:
          noneCnt += 1
      if (noneCnt != cols):
        if (cnt > 0):
          avgList[rowIdx] = sum / float(cnt)
        sumList[rowIdx] = sum
        cntList[rowIdx] = cnt

    cols = len(self.compList)
    result = {}
    result['TEXT' ] = self.compList
    result['ROWS'] = rows
    result['COLS'] = cols
    #result['SUM' ] = sumList
    #result['AVG' ] = avgList
    #result['CNT' ] = cntList
    result['DATA'] = [[None for col in range(cols)] for row in range(rows)]
    result['RHDR'] = None
    result['CHDR'] = [[None for col in range(cols)] for row in range(   1)]
    for rowIdx in range(rows):
      for colIdx in range(cols):
        result['DATA'][rowIdx][0] = avgList[rowIdx]
        result['DATA'][rowIdx][1] = sumList[rowIdx]
        result['DATA'][rowIdx][2] = cntList[rowIdx]
        result['CHDR'][0][colIdx] = self.compList[colIdx]

    return result

  #--------------------------------------------------------------------
  def _calcColMetrics(self,data):
    rows = len(data)
    cols = len(data[0])

    sumList = [None for col in range(cols)]
    avgList = [None for col in range(cols)]
    cntList = [None for col in range(cols)]
    for colIdx in range(cols):
      sum     = 0.0
      avg     = 0.0
      cnt     =   0
      noneCnt =   0
      for rowIdx in range(rows):
        if (data[rowIdx][colIdx] != None):
          sum += float(data[rowIdx][colIdx])
          cnt += 1
        else:
          noneCnt += 1
      if (noneCnt != rows):
        if (cnt > 0):
          avgList[colIdx] = sum / float(cnt)
        sumList[colIdx] = sum
        cntList[colIdx] = cnt

    rows = len(self.compList)
    result = {}
    #result['RHDR'] = self.compList
    result['ROWS'] = rows
    result['COLS'] = cols
    #result['SUM' ] = sumList
    #result['AVG' ] = avgList
    #result['CNT' ] = cntList
    result['DATA'] = [[None for col in range(cols)] for row in range(rows)]
    result['RHDR'] = [[None for col in range(   1)] for row in range(rows)]
    result['CHDR'] = None
    for rowIdx in range(rows):
      result['RHDR'][rowIdx][0] = self.compList[rowIdx]
      for colIdx in range(cols):
        result['DATA'][0][colIdx] = avgList[colIdx]
        result['DATA'][1][colIdx] = sumList[colIdx]
        result['DATA'][2][colIdx] = cntList[colIdx]

    return result

  #--------------------------------------------------------------------
  def _calcTblMetrics(self,data):
    rows = len(data)
    cols = len(data[0])

    sumList = [None for col in range(cols)]
    avgList = [None for col in range(cols)]
    cntList = [None for col in range(cols)]
    for colIdx in range(cols):
      sum     = 0.0
      avg     = 0.0
      cnt     =   0
      noneCnt =   0
      for rowIdx in range(rows):
        if (data[rowIdx][colIdx] != None):
          sum += float(data[rowIdx][colIdx])
          cnt += 1
        else:
          noneCnt += 1
      if (noneCnt != rows):
        if (cnt > 0):
          avgList[colIdx] = sum / float(cnt)
        sumList[colIdx] = sum
        cntList[colIdx] = cnt

    rows = len(self.compList)
    result = {}
    #result['CHDR'] = self.compList
    result['ROWS'] = rows
    result['COLS'] = cols
    #result['SUM' ] = sumList
    #result['AVG' ] = avgList
    #result['CNT' ] = cntList
    result['DATA'] = [[None for col in range(cols)] for row in range(rows)]
    result['RHDR'] = None
    result['CHDR'] = [[None for col in range(cols)] for row in range(   1)]
    for rowIdx in range(rows):
      for colIdx in range(cols):
        result['DATA'][0][colIdx] = avgList[colIdx]
        result['DATA'][1][colIdx] = sumList[colIdx]
        result['DATA'][2][colIdx] = cntList[colIdx]
        result['CHDR'][0][colIdx] = self.compList[colIdx]

    return result

  #--------------------------------------------------------------------
  def _calcTblMetrics(self,data):
#    rows = len(data)
#    cols = len(data[0])
#
#    sumList = [None for col in range(cols)]
#    avgList = [None for col in range(cols)]
#    cntList = [None for col in range(cols)]
#    for colIdx in range(cols):
#      sum = 0.0
#      avg = 0.0
#      cnt =   0
#      for rowIdx in range(rows):
#        if (data[rowIdx][colIdx] != None):
#          sum += float(data[rowIdx][colIdx])
#          cnt += 1
#      if (cnt > 0):
#        avgList[colIdx] = sum / float(cnt)
#      sumList[colIdx] = sum
#      cntList[colIdx] = cnt
#
#    result = {}
#    result['ROWS'] = 3
#    result['COLS'] = cols
#    result['SUM' ] = sumList
#    result['AVG' ] = avgList
#    result['CNT' ] = cntList
#    result['DATA'] = [sumList,avgList,cntList] 

    return None


