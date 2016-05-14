import logging
from   database.database            import Database as Db
from   summary.matrix.matrixdata    import MatrixData
from   database.queries.getweeks    import GetWeeks
from   database.queries.getgkasum   import GetGkaSum


#----------------------------------------------------------------------
class GkaData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,type,period):

    super().__init__()

    regionList = super().calcRegionList(region)

    codeList = ['ERC','NOK','ALU','OTHERS','COB','TTT','OTH']

    weekDict = GetWeeks(Db.db,regionList,period)
    dataList = GetGkaSum(Db.db,regionList,weekDict,codeList)

    weekCnt = len(dataList)
    itemCnt = len(dataList[0])

    hours = [[None for j in range(itemCnt)] for i in range(weekCnt)]
    for week in range(weekCnt):
      for item in range(itemCnt):
        if (dataList[week] != None):
          tup = dataList[week][item]
          code = tup[0]
          hrs  = tup[1]
          if (code != codeList[item]):
            logging.error('Code and CodeList don\'t match: ' + code + ' ' + codeList[item])
            hours[week][item] = None
          else:
            hours[week][item] = float(hrs)
        else:
          hours[week][item] = None

    self.data.AddData(hours)

    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)

    self.colCompHdr.AddData(['Avg'])
    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
    super().calcTitle('Global Key Accounts and Other',regionList,period)
    
    rowHdrData = ['Ericsson','Nokia','Alcatel-Lucent','Sum of all other customers', \
                    'Cobham', 'Technical Training - All Types','Customer \'Other\'']
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

#    rowAvgList = super().calcRowAvg(super().calcRowSum(hours))
#    self.colCompData.AddData(rowAvgList,cols=1,rows=itemCnt)
#
#    self.colCompHdr.AddData(['Avg'])
#    self.colHdr.AddData(super().calcWeekNumTextList(weekDict['MAX']))
#    super().calcTitle('Utilisation (On Pre-Sales Works)',regionList,period)
#    self.title.fmt['fill'] = 'Orange 1'
#    
#    rowHdrData = ['For','Total Time','Utilisation as a %']
#    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)



#    codes = ['ERC','NOK','ALU','OTHERS','COB','TTT','OTH']
#
#    weekList = Db.WeeksTbl.GetWeeks(Db.db,period)
#    data = Db.TsEntryTbl.GetGkaSum(Db.db,region,codes,weekList)
#
#    colSumList = super().calcColSum(data)
#    rowSumList = super().calcRowSum(data)
#    weeks      = super().calcCols(colSumList)
#    if (weeks != len(weekList)):
#      weeks = len(weekList)
#    rowAvgList = super().calcRowAvg(rowSumList,weeks)
#
#    self.compData = [rowAvgList]
#    self.data     = super().calcData(data,len(codes),weeks)
#
#    self.dataCols = len(self.data)
#    self.dataRows = len(self.data[0])
#
#
#    self.title = 'Customers'
#    self.colDesc = []
#    for i in range(self.dataCols):
#      self.colDesc.append('Week ' + str(i+1))
#
#    self.colCompDesc = ['Avg']
#
#    self.rowDesc = ['Ericsson','Nokia','Alcatel-Lucent','Sum of all other customers', \
#                    'Cobham', 'Technical Training - All Types','Customer \'Other\'']
#    #for i in range(self.dataRows):
#    #  self.rowDesc.append(self.rowDesc)
#
#    self.rowCompDesc = []