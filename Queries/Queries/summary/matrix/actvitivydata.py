import logging
from   database.database               import Database as Db
from   summary.matrix.matrixdata       import MatrixData
from   database.queries.getweeks       import GetWeeks
from   database.queries.getactivities  import GetActivities
from   database.queries.getactivitysum import GetActivitySum

#----------------------------------------------------------------------
class ActivityData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__(region,mType,period)

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    actList  = GetActivities(Db.db,'')
    dataList = GetActivitySum(Db.db,regionList,weekDict,actList)

    weekCnt = len(dataList)
    itemCnt = len(dataList[0])

    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
    for week in range(weekCnt):
      for item in range(itemCnt):
        if (dataList[week] != None):
          hours[week][item] = float(dataList[week][item][2])
        else:
          hours[week][item] = None

    self.data.AddData(hours)

    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)

    self.colCompHdr.AddData(['Avg'])
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcTitle('Activity',regionList,period)

    rowHdrData = []
    for item in actList:
      text = item[1] + ' - ' + str(item[0])
      rowHdrData.append(text)
    rowHdrData.append('Other (leave, overhead, etc.)')

    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

    gFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    oFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1'}
    nFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
    gSet = set([10,11,14,15,16,17,18,23])
    self.rowHdr.fmt = []
    for item in actList:
      if (item[0] in gSet):
        self.rowHdr.fmt.append(gFmt)
      else:
        self.rowHdr.fmt.append(oFmt)
    self.rowHdr.fmt.append(nFmt)

#    colSumList = super().calcColSum(data)
#    rowSumList = super().calcRowSum(data)
#    weeks      = super().calcCols(colSumList)
#    if (weeks != len(weekList)):
#      weeks = len(weekList)
#    rowAvgList = super().calcRowAvg(rowSumList,weeks)
#
#    self.compData = [rowAvgList]
#    self.data     = super().calcData(data,len(actList),weeks)
#
#    self.dataCols = len(self.data)
#    self.dataRows = len(self.data[0])
#
#    self.title = 'Activity'
#    self.colDesc = []
#    for i in range(self.dataCols):
#      self.colDesc.append('Week ' + str(i+1))
#
#    self.colCompDesc = ['Avg']

#    gSet = set([10,11,14,15,16,17,18,23])
#    self.rowDesc = []
#    self.descRowFmt = []
#    gFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
#    oFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1'}
#    for i in range(self.dataRows):
#      self.rowDesc.append(actList[i][1] + '-' + str(actList[i][0]))
#      if (actList[i][0] in gSet):
#        self.descRowFmt.append(gFmt)
#      else:
#        self.descRowFmt.append(oFmt)
#
#    self.rowCompDesc = []


