import logging
from   database.database             import Database as Db
from   database.queries.getfaelist   import GetFaeList
from   database.queries.getfaeawhsum import GetFaeAwhSum
from   summary.matrix.matrixdata     import MatrixData

#----------------------------------------------------------------------
class FaeAwhData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__()

    if (type(region) is list):
      if ('ALL' in region):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = region
    else:
      if (region == 'ALL'):
        regionList = ['EMEA','AM','GC']
      else:
        regionList = [region]

    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    result   = GetFaeAwhSum(Db.db,regionList,weekList)

    faeList  = result.faeList
    weekList = result.weekList

    faeCnt = len(faeList)
    weekCnt = len(weekList)

#    headCntList = []
#    workDaysList = []
#    data = [[None for i in range(faeCnt)] for j in range(weekCnt)]
#    for i in range(weekCnt):
#      headCntList.append(weekList[i].headCount)
#      workDaysList.append(weekList[i].workingDays)
#      for j in range(faeCnt):
#        fname = faeList[j].fname
#        lname = faeList[j].lname
#        tup   = weekList[i].hours[j]
#        if (fname != tup[0] and lname != tup[1]):
#          logging.error('Database corrupt matching FAE names')
#          return None
#        data[i][j] = tup[2]
#
#    self.data.data = super().calcData(data,faeCnt,weekCnt)
#    self.data.cols = weekCnt
#    self.data.rows = faeCnt

    super().calcFaeData(faeList,faeCnt,weekList,weekCnt)
    super().calcFaeColCompData(self.data.data,faeList,faeCnt,regionList)
    super().calcFaeRowCompData(self.data.data,faeList,faeCnt,weekList,weekCnt,regionList)

#    rowAvgList = super().calcRowAvg(super().calcRowSum(data))
#    colAvgList = super().calcColAvg(super().calcColSum(data))
#    conHrsList = []
#    maxHrsList = []
#    faeRgnList = []
#    for fae in faeList:
#      conHrsList.append(fae.nrmHrs)
#      maxHrsList.append(fae.maxHrs)
#      if (len(regionList) > 1):
#        faeRgnList.append(fae.region)
#
#    if (len(regionList) > 1):
#      self.colCompData.data = [rowAvgList,conHrsList,maxHrsList,faeRgnList]
#    else:
#      self.colCompData.data = [rowAvgList,conHrsList,maxHrsList]
#    self.colCompData.cols = len(self.colCompData.data)
#    self.colCompData.rows = faeCnt
#
#    super().calcFaeColCompHdr(regionList,['Avg','Contracted\rHours',{'EMEA':'EUWTD','OTHER':'Max Hours'}])

#    compDataFmt = {'hAlign':'R','vAlign':'C','border':{'A':'thin'},'numFmt':'0'}
#    self.rowCompData.fmt = compDataFmt
#    self.rowCompData.data = [[] for i in range(weekCnt)]
#    for i in range(weekCnt):
#      self.rowCompData.data[i].append(colAvgList[i])
#      self.rowCompData.data[i].append(headCntList[i])
#      if ('AM' in regionList):
#        self.rowCompData.data[i].append(workDaysList[i].am_days)
#      if ('EMEA' in regionList):
#        self.rowCompData.data[i].append(workDaysList[i].uk_days)
#        self.rowCompData.data[i].append(workDaysList[i].fr_days)
#        self.rowCompData.data[i].append(workDaysList[i].de_days)
#        self.rowCompData.data[i].append(workDaysList[i].fi_days)
#        self.rowCompData.data[i].append(workDaysList[i].se_days)
#      if ('GC' in regionList):
#        self.rowCompData.data[i].append(workDaysList[i].gc_days)
#
#    self.rowCompData.rows = len(self.rowCompData.data[0])
#    self.rowCompData.cols = weekCnt

#    self.rowCompHdr.data = []
#    self.rowCompHdr.data.append('Week Average')
#    self.rowCompHdr.data.append('HeadCount')
#    if ('AM' in regionList):
#      self.rowCompHdr.data.append('AM Working Days')
#    if ('EMEA' in regionList):
#      self.rowCompHdr.data.append('UK Working Days')
#      self.rowCompHdr.data.append('FR Working Days')
#      self.rowCompHdr.data.append('DE Working Days')
#      self.rowCompHdr.data.append('FI Working Days')
#      self.rowCompHdr.data.append('SE Working Days')
#    if ('GC' in regionList):
#      self.rowCompHdr.data.append('GC Working Days')
#
#    self.rowCompHdr.rows = len(self.rowCompHdr.data)

    super().calcFaeColCompHdr(regionList,['Avg','Contracted\rHours',{'EMEA':'EUWTD','OTHER':'Max Hours'}])
    super().calcFaeRowCompHdr(regionList)

    super().calcFaeTitle('Actual Working Hours (exc Leave/Holiday)',regionList,period)
    super().calcFaeColHdr()
    super().calcFaeRowHdr(faeList)



