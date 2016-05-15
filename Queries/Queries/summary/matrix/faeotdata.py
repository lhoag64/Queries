import logging
from   database.database            import Database as Db
from   database.queries.getweeks    import GetWeeks
from   database.queries.getfaeotsum import GetFaeOtSum
from   database.queries.faedata     import FaeHoursData
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class FaeOtData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__(region,mType,period)

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    dbResult = GetFaeOtSum(Db.db,regionList,weekDict)

    faeList = dbResult.faeList
    rawList = dbResult.hoursList

    faeDict = {}
    for fae in faeList:
      tup = (fae.fname,fae.lname)
      if (tup not in faeDict):
        faeDict[tup] = fae

    dataList = []
    for week in rawList:
      hoursList = []
      if (week.hours != None):
        for hours in week.hours:
          name  = (hours[0],hours[1])
          wkHrs = hours[2]
          lvHrs = hours[3]
          nmHrs = hours[4]
          if (wkHrs != None and lvHrs != None):
            if (lvHrs == 0.0):
              ot = wkHrs - nmHrs
            else:
              ot = wkHrs + lvHrs - nmHrs
            if (ot < 0.0):
              ot = 0.0
            #text  = ''
            #text += '|' + (hours[0] + ' ' + hours[1]).ljust(30)
            #text += '|W:' + str(wkHrs).rjust(5) + '|N:' + str(nmHrs).rjust(5) + '|L:' + str(lvHrs).rjust(5) + '|OT:' + str(ot).rjust(5)
            #logging.debug(text)
            tup = (hours[0],hours[1],ot)
            hoursList.append(tup)
          else:
            tup = (hours[0],hours[1],None)
            hoursList.append(tup)
        dataList.append(FaeHoursData(week.workingDays,week.headCount,hoursList))
      else:
        dataList.append(FaeHoursData(None,None,None))

    faeCnt  = len(faeList)
    weekCnt = len(dataList)

    super().calcFaeData(faeList,faeCnt,dataList,weekCnt)
    super().calcFaeColCompData(self.data.data,faeList,faeCnt,regionList)
    super().calcFaeRowCompData(self.data.data,faeList,faeCnt,dataList,weekCnt,regionList)

    super().calcFaeColCompHdr(regionList,['Avg','Contracted\rHours',{'EMEA':'EUWTD','OTHER':'Max Hours'}])
    super().calcFaeRowCompHdr(regionList)

    self.title.AddData(super().calcTitleText('Additional Hours',regionList,period))
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcFaeRowHdr(faeList)
    #super().calcTitle('Additional Hours',regionList,period)
    #super().calcColHdr()

#    1Gsuper().__init__()
#
#    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
#    faeList  = Db.TsEntryTbl.GetFaeList(Db.db,region,period)
#
#    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
#    result   = Db.TsEntryTbl.GetFaeOtSum(Db.db,region,weekList)
#
#    faeDict = {}
#    for fae in faeList:
#      if ((fae[0],fae[1]) not in faeDict):
#        faeDict[(fae[0],fae[1])] = [fae[2],fae[3],fae[4]]
#
#    data = [[None for i in range(len(result[0]))] for j in range(len(result))]
#    for i in range(len(result)):
#      for j in range(len(result[0])):
#        fname = result[i][j][0]
#        lname = result[i][j][1]
#        wkHrs = result[i][j][2]
#        lvHrs = result[i][j][3]
#        nmHrs = float(faeDict[(fname,lname)][0])
#        data[i][j] = wkHrs - nmHrs + lvHrs
#        #text  = '|' + lname.ljust(14) + '|'
#        #text += str(wkHrs).rjust(5) + '|' + str(lvHrs).rjust(5) + '|' + str(nmHrs).rjust(5) + '||'
#        #text += str(data[i][j]).rjust(5) + '|'
#        #logging.debug(text)
#      pass
#
#    colSumList = super().calcColSum(data)
#    rowSumList = super().calcRowSum(data)
#    weeks      = super().calcCols(colSumList)
#    if (weeks != len(weekList)):
#      weeks = len(weekList)
#
#    rowAvgList = super().calcRowAvg(rowSumList,weeks)
#
#    self.compData = [rowAvgList]
#
#    self.data     = super().calcData(data,len(faeList),weeks)
#
#    self.dataCols = len(self.data)
#    self.dataRows = len(self.data[0])
#
#    self.title = 'Additional Hours'
#    self.colDesc = []
#    for i in range(self.dataCols):
#      self.colDesc.append('Week ' + str(i+1))
#
#    self.compCols = len(self.compData)
#    self.colCompDesc = ['Avg']
#
#    self.rowDesc = []
#    for fae in faeList:
#      self.rowDesc.append(fae[0] + ' ' + fae[1])
#
#    self.rowCompDesc = []
#