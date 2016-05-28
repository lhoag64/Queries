import logging
from   collections import OrderedDict

#----------------------------------------------------------------------
class SummaryData:
  def __init__(self,itemDict,nameDict):
    for item in itemDict:
      logging.debug(item)
    for name in nameDict:
      logging.debug(name)

    logging.debug()