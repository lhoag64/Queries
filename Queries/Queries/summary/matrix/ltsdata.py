import logging
from   database.database          import Database as Db
from   summary.matrix.matrixdata  import MatrixData
from   database.queries.getweeks  import GetWeeks
from   database.queries.getlts    import GetLts
from   database.queries.getltssum import GetLtsSum
#----------------------------------------------------------------------
class LtsData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__(region,mType,period)

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    ltsList  = GetLts(Db.db,'')
    dataList = GetLtsSum(Db.db,regionList,weekDict,ltsList)

    weekCnt = len(dataList)
    itemCnt = len(dataList[0])

    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
    for week in range(weekCnt):
      for item in range(itemCnt):
        if (dataList[week] != None):
          hours[week][item] = float(dataList[week][item][1])
        else:
          hours[week][item] = None

    self.data.AddData(hours)

    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)

    self.colCompHdr.AddData(['Avg'])
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcTitle('Labour vs Travel',regionList,period)

    rowHdrData = []
    for item in ltsList:
      rowHdrData.append(item[0])
    rowHdrData.append('Other')

    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

#    gFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
#    oFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1'}
#    nFmt = {'hAlign':'L','vAlign':'C','border':{'A':'thin'}}
#    gSet = set([10,11,14,15,16,17,18,23])
#    self.rowHdr.fmt = []
#    for item in actList:
#      if (item[0] in gSet):
#        self.rowHdr.fmt.append(gFmt)
#      else:
#        self.rowHdr.fmt.append(oFmt)
#    self.rowHdr.fmt.append(nFmt)

'''
    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
    lts      = Db.TsLtsTbl.GetLts(Db.db,'ALL')

    data = Db.TsEntryTbl.GetLtsSum(Db.db,region,lts,weekList)

    colSumList = super().calcColSum(data)
    rowSumList = super().calcRowSum(data)
    weeks      = super().calcCols(colSumList)
    if (weeks != len(weekList)):
      weeks = len(weekList)
    rowAvgList = super().calcRowAvg(rowSumList,weeks)

    self.compData = [rowAvgList]
    self.data     = super().calcData(data,len(lts),weeks)

    self.dataCols = len(self.data)
    self.dataRows = len(self.data[0])

    self.title = 'Labour vs Travel'
    self.colDesc = []
    for i in range(self.dataCols):
      self.colDesc.append('Week ' + str(i+1))

    self.colCompDesc = ['Avg']

    self.rowDesc = []
    for i in range(self.dataRows):
      self.rowDesc.append(lts[i][0])

    self.rowCompDesc = []

'''


