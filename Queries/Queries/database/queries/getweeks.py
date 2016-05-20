#import logging
#import datetime
#import sqlite3
#
#WeekTable =                                  \
#  {                                          \
#    'JAN'     : ('2016-01-04','2016-01-31'), \
#    'FEB'     : ('2016-02-01','2016-02-28'), \
#    'MAR'     : ('2016-02-29','2016-04-03'), \
#    'APR'     : ('2016-04-04','2016-05-01'), \
#    'MAY'     : ('2016-05-02','2016-05-29'), \
#    'JUN'     : ('2016-05-30','2016-07-03'), \
#    'JUL'     : ('2016-07-04','2016-05-32'), \
#    'Q1FY2016': ('2016-01-04','2016-04-03'), \
#    'H1FY2016': ('2016-01-04','2016-07-03')  \
#  }
#   
##----------------------------------------------------------------------
#def GetWeeks(db,regionList,period):
#
#  c = db.cursor()
#
#  weekList = {}
#
#  regions = regionList.copy()
#  regions.append('MAX')
#  for region in regions:
#    sqlopt  = []
#    sqltxt  = 'SELECT MAX(ts.entry_date)'
#    sqltxt += '  FROM ts_entry AS ts'
#    if (region != 'MAX'):
#      sqltxt += '  WHERE ts.region = \'' + region + '\''
#
#    c.execute(sqltxt,tuple(sqlopt))
#    dbResult = c.fetchall()
#
#    now = datetime.date.today().strftime("%Y-%m-%d")
#    max = dbResult[0][0]
#
#    weekStart = '2016-01-04'
#    weekEnd   = max
#
#    if (period != 'ALL'):
#      if (period in WeekTable):
#        weekStart = WeekTable[period][0]
#        weekEnd   = WeekTable[period][1]
#        if (weekEnd > max):
#          weekEnd = max
#      else:
#        logging.error('Invalid period:' + period)
#        weekEnd = weekStart
#
#    sqlopt  = [weekStart,weekEnd]
#    sqltxt  = 'SELECT wc_date,week'
#    sqltxt += '  FROM weeks'
#    sqltxt += '  WHERE wc_date >= ? and wc_date <= ?'
#
#    c.execute(sqltxt,tuple(sqlopt))
#    dbResult = c.fetchall()
#
#    weekList[region] = []
#    for item in dbResult:
#      weekList[region].append(item)
#
#    minCnt = 100
#    minRgn = None
#    for region in weekList:
#      cnt = len(weekList[region])
#      if (cnt < minCnt):
#        minCnt = cnt
#        minRgn = region
#
#  weekList['MIN'] = weekList[minRgn]
#
#  return weekList
#
##----------------------------------------------------------------------
#def GetWeekNumbers(db,period):
#
#  c = db.cursor()
#  c.execute('SELECT MAX(entry_date) FROM ts_entry')
#  resultList = c.fetchall()
#
#  now = datetime.date.today().strftime("%Y-%m-%d")
#  max = resultList[0][0]
#
#  weekStart = '2016-01-04'
#  weekEnd   = max
#
#  if (period != 'ALL'):
#    if (period in WeekTable):
#      weekStart = WeekTable[period][0]
#      weekEnd   = WeekTable[period][1]
#      if (weekEnd > max):
#        weekEnd = max
#    else:
#      logging.error('Invalid period:' + period)
#      weekEnd = weekStart
#
#  c.execute \
#    ( \
#      '''
#         SELECT week FROM weeks
#         WHERE wc_date >= ? and wc_date <= ?
#      '''
#    ,(weekStart,weekEnd))
#
#  resultList =  c.fetchall()
#  return resultList
###