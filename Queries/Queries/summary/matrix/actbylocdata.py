import logging
from   database.database               import Database as Db
from   summary.matrix.matrixdata       import MatrixData
from   database.queries.getweeks       import GetWeeks
from   database.queries.getactbylocsum import GetActByLocSum

#----------------------------------------------------------------------
class ActByLocData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period,**kwargs):

    act = None
    opt = kwargs['opt']
    if (opt):
      if ('ACT' in opt):
        act = opt['ACT']
    if (act == None):
      logging.error('Activity by Location requres activity argument, skipping')
      return

    super().__init__(region,mType,period)

    self.name += '_' + str(act).zfill(2)

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    dataDict = GetActByLocSum(Db.db,regionList,weekDict,act)

    dataList = dataDict['HRSLIST']

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
    super().calcTitle(dataDict['TITLE'],regionList,period)

    rowHdrData = []
    for item in dataDict['GRPLIST']:
      rowHdrData.append(item[1])
    
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

#    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
#    actList  = Db.TsActTbl.GetActivities(Db.db,'ALL')
#
#    act     = kwargs['act']
#    locList = kwargs['loc']
#
#    data = Db.TsEntryTbl.GetActByLocSum(Db.db,region,act,locList,weekList)
#
#    actDesc = ''
#    for item in actList:
#      if (item[0] == act):
#        actDesc = item[1]
#        break
#    title = actDesc + ' - ' + str(act)
#
#    colSumList = super().calcColSum(data)
#    rowSumList = super().calcRowSum(data)
#    weeks      = super().calcCols(colSumList)
#    if (weeks != len(weekList)):
#      weeks = len(weekList)
#    rowAvgList = super().calcRowAvg(rowSumList,weeks)
#
#    self.compData = [rowAvgList]
#    self.data     = super().calcData(data,len(locList),weeks)
#
#    self.dataCols = len(self.data)
#    self.dataRows = len(self.data[0])
#
#
#    self.title = title
#    self.colDesc = []
#    for i in range(self.dataCols):
#      self.colDesc.append('Week ' + str(i+1))
#
#    self.colCompDesc = ['Avg']
#
#    self.rowDesc = locList
#
#    self.rowCompDesc = []