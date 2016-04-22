import logging
from   xlinterface                import WrkBook
from   xlinterface                import WrkSheet
from   summary.matrix.matrixsheet import MatrixSheet

#----------------------------------------------------------------------
class Summary:
  def __init__(self):
    self.wsDict = {}
    self.wb = WrkBook()
    ws = self.wb.GetActiveSheet()
    self.wb.SetName(ws,'Summary')
    self.wsDict['Summary'] = ws

  #--------------------------------------------------------------------
  def AddMatrix(self,region,type,period):
    name = region + type + period
    ws = self.wb.CreateSheet(name)
    matrix = MatrixSheet(ws,region,type,period)
    self.wsDict[name] = ('Matrix',matrix,ws)
    
  #--------------------------------------------------------------------
  def Save(self,filename):
    self.wb.Save(filename)
