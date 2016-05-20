import logging
from   summary.summaryitem          import SummaryItem
from   database.database            import Database as Db
from   summary.matrix.matrixdata    import MatrixData
#from   database.queries.getweeks    import GetWeeks
from   database.queries.getgkasum   import GetGkaSum


#----------------------------------------------------------------------
class GkaData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,item):

    super().__init__(item)

    regionList = super().calcRegionList(self.region)

    codeList = ['ERC','NOK','ALU','OTHERS','COB','TTT','OTH']

    weekDict = GetWeeks(Db.db,regionList,self.period)
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
    super().calcTitle('Global Key Accounts and Other',regionList,self.period)
    
    rowHdrData = ['Ericsson','Nokia','Alcatel-Lucent','Sum of all other customers', \
                    'Cobham', 'Technical Training - All Types','Customer \'Other\'']
    self.rowHdr.AddData(rowHdrData,cols=1,rows=itemCnt)

    super().calcSize()

    self.rangeList = []
