import logging
from   summary.summaryitem          import SummaryItem
from   database.database            import Database as Db
#from   database.queries.getweeks    import GetWeeks
#from   database.queries.getfaeotsum import GetFaeOtSum
from   database.queries.faedata     import FaeHoursData
from   summary.matrix.matrixdata    import MatrixData

#----------------------------------------------------------------------
class FaeOtData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    regionList = super().calcRegionList(self.region)

    weekDict = GetWeeks(Db.db,regionList,self.period)
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

    self.title.AddData(super().calcTitleText('Additional Hours',regionList,self.period))
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcFaeRowHdr(faeList)

    super().calcSize()

    self.rangeList = []
