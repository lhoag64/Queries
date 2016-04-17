import sys
import logging
import threading
import time

#----------------------------------------------------------------------
def LogConfig(name):
 
  with open(name,'w') as file:
    pass

  logfmt = '%(asctime)s-%(levelname)s-%(message)s'
  format = logging.Formatter(logfmt)
  logging.basicConfig(level=logging.DEBUG,format=logfmt)
 
  log = logging.getLogger()
  fh  = logging.FileHandler(name)
  fh.setFormatter(format)
  log.addHandler(fh)

