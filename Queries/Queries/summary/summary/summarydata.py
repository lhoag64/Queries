import logging
from   collections     import OrderedDict
from   summary.objdata import ObjData
#----------------------------------------------------------------------
class SummaryData(ObjData):
  def __init__(self,item,itemDict,nameDict,objNameDict):

    super().__init__(item)

    self.itemDict    = itemDict
    self.nameDict    = nameDict
    self.objNameDict = objNameDict

    self.fmt1a = {'hAlign':'C','vAlign':'C','wrap':True,'font':{'emph':'B','size':14}}

    self.fmt2a = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Blue 2','numFmt':'General','font':{'emph':'B','size':11}}
    self.fmt2b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 2','numFmt':'General','font':{'emph':'B','size':11}}
    self.fmt2c = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3','numFmt':'General','font':{'emph':'B','size':11}}
    self.fmt2f = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3','numFmt':'0.0'    ,'font':{'emph':'B','size':11}}
    self.fmt2i = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3','numFmt':'0'      ,'font':{'emph':'B','size':11}}
    self.fmt2g = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3','numFmt':'General','font':{'emph':'B','size':11}}
    self.fmt2d = {'F':self.fmt2f,'I':self.fmt2i,'G':self.fmt2g}
    self.fmt3  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3'}
    self.fmt3a = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3'}
    self.fmt3b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Blue 3','numFmt':'0.0','font':{'emph':'B'}}
    self.fmt4  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Green 1'}
    self.fmt4b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Green 1','numFmt':'0.0','font':{'emph':'B'}}
    self.fmt5  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1'}
    self.fmt5b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Orange 1','numFmt':'0.0','font':{'emph':'B'}}
    self.fmt6  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Red 1'}
    self.fmt6b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Red 1','numFmt':'0.0','font':{'emph':'B'}}
    self.fmt7  = {'hAlign':'L','vAlign':'C','border':{'A':'thin'},'fill':'Yellow 1'}
    self.fmt7b = {'hAlign':'C','vAlign':'C','border':{'A':'thin'},'fill':'Yellow 1','numFmt':'0.0','font':{'emph':'B'}}



   