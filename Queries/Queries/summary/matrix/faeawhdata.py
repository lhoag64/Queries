import logging
from   database.database             import Database as Db
from   database.queries.getfaeawhsum import GetFaeAwhSum
from   database.queries.getweeks     import GetWeeks
from   summary.matrix.matrixdata     import MatrixData

#----------------------------------------------------------------------
class FaeAwhData(MatrixData):
#----------------------------------------------------------------------
  def __init__(self,region,mType,period):

    super().__init__()

    regionList = super().calcRegionList(region)

    weekDict = GetWeeks(Db.db,regionList,period)
    dbResult = GetFaeAwhSum(Db.db,regionList,weekDict)

    faeList  = dbResult.faeList
    dataList = dbResult.hoursList

    faeCnt  = len(faeList)
    weekCnt = len(dataList)

    super().calcFaeData(faeList,faeCnt,dataList,weekCnt)
    super().calcFaeColCompData(self.data.data,faeList,faeCnt,regionList)
    super().calcFaeRowCompData(self.data.data,faeList,faeCnt,dataList,weekCnt,regionList)

    super().calcFaeColCompHdr(regionList,['Avg','Contracted\rHours',{'EMEA':'EUWTD','OTHER':'Max Hours'}])
    super().calcFaeRowCompHdr(regionList)

    super().calcFaeTitle('Actual Working Hours (exc Leave/Holiday)',regionList,period)
    super().calcFaeColHdr()
    super().calcFaeRowHdr(faeList)



