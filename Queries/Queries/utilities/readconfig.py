import logging
import os.path
import csv
from   collections import OrderedDict

#----------------------------------------------------------------------
def parseWorkDir(fileline,cfgDict,row):
  if (len(row) != 2):
    logging.error('Error in config file, invalid TSDIR definition at line: ' + str(fileline))
    logging.error('  Format: TSDIR, dir-name')
    exit(0)

  if (os.path.isdir(row[1]) != True):
    logging.error('Can\'t locate WORKDIR: ' + row[1] + 'at line: ' + str(fileline))
    exit(0)

  cfgDict['WORKDIR'] = row[1]

#----------------------------------------------------------------------
def parseDatabase(fileline,cfgDict,row):
  if (len(row) != 2):
    logging.error('Error in config file, invalid DATABASE definition at line: ' + str(fileline))
    logging.error('  Format: DATABASE, workbook-pathname')
    exit(0)

  if (os.path.isfile(row[1]) != True):
    logging.error('Can\'t locate DATABASE: ' + row[1] + 'at line: ' + str(fileline))
    exit(0)

  cfgDict['DATABASE'] = row[1]

#----------------------------------------------------------------------
def parseWorkbook(fileline,cfgDict,row):
  if (len(row) != 3):
    logging.error('Error in config file, invalid WORKBOOK definition at line: ' + str(fileline))
    logging.error('  Format: WORKBOOK, formal-name, database-pathname')
    exit(0)

  row1 = row[1].upper()

  if ('WKBOOKS' not in cfgDict):
    cfgDict['WKBOOKS'] = OrderedDict()
  if (row1 not in cfgDict['WKBOOKS']):
    cfgDict['WKBOOKS'][row1] = OrderedDict()
    cfgDict['WKBOOKS'][row1]['FILENAME'] = row[2]
    cfgDict['WKBOOKS'][row1]['WKSHEETS'] = OrderedDict()
  else:
    logging.error('Duplicate workbook: ' + row[1] + 'at line: ' + str(fileline))
    exit(0)

  return row1

#----------------------------------------------------------------------
def parseWorksheet(fileline,cfgDict,row,curWb):
  if (len(row) != 3):
    logging.error('Error in config file, invalid WORKSHEET definition at line: ' + str(fileline))
    logging.error('  Format: WORKSHEET, formal-name, description')
    exit(0)

  row1 = row[1].upper()

  if (row1 not in cfgDict['WKBOOKS'][curWb]['WKSHEETS']):
    cfgDict['WKBOOKS'][curWb]['WKSHEETS'][row1] = OrderedDict()
    cfgDict['WKBOOKS'][curWb]['WKSHEETS'][row1]['NAME'] = row[2]
    cfgDict['WKBOOKS'][curWb]['WKSHEETS'][row1]['OBJS'] = OrderedDict()
  else:
    logging.error('Duplicate worksheet: ' + row[1] + 'at line: ' + str(fileline))
    exit(0)

  return row1

#----------------------------------------------------------------------
def parseObj(fileline,cfgDict,row,curWb,curWs):
  #--------------------------------------------------------------------
  def parseLoc(text):
    stxt = ''
    for ch in text:
      if (ch not in ['(',')']):
        stxt += ch
    stxt = stxt.strip().split(' ')
    return (stxt[0].strip(),stxt[1].strip())

  #--------------------------------------------------------------------
  def parseDict(tgt,text):
    tmp = ''
    for ch in text:
      if (ch not in ['\'','{','}']):
        tmp += ch
    tmp = tmp.split(':')
    tgt[tmp[0]] = tmp[1]

  #--------------------------------------------------------------------
  if (len(row) != 7):
    logging.error('Error in config file, invalid object definition at line: ' + str(fileline))
    logging.error('  Format: MATRIX, location, region, period, formal-name, opt1, opt2')
    exit(0)

  row0 = row[0].upper()
  row1 = parseLoc(row[1])
  row2 = row[2].upper()
  row3 = row[3].upper()
  row4 = row[4].upper()
  row5 = row[5].upper()
  row6 = row[6].upper()
  if (row5 == 'NONE'): row5 = None
  if (row6 == 'NONE'): row6 = None

  name = row0 + '-' + row2 + '-' + row3 + '.' + row4
  if (row5 != None):
    name += '.' + row5

  if (name not in cfgDict['WKBOOKS'][curWb]['WKSHEETS'][curWs]['OBJS']):
    if (row6 != None):
      row6 = {}
      parseDict(row6,row[6])
    tup = (row1,row0,row2,row3,row4,row5,row6,name)
    cfgDict['WKBOOKS'][curWb]['WKSHEETS'][curWs]['OBJS'][name] = tup
  else:
    logging.error('Duplicate object: ' + row[0] + 'at line: ' + str(fileline))
    exit(0)

#----------------------------------------------------------------------
def ReadConfig(filename):

  fileline = 1

  cfgDict = {}

  with open(filename,'r') as fp:
    reader = csv.reader(fp)
    for inprow in reader:
      if ((len(inprow) == 0) or (inprow[0][:1] == '#')):
        continue
      row = []
      for item in inprow:
        row.append(item.strip())

      keyword = row[0].upper()
      if (keyword == 'WORKDIR'):
        parseWorkDir(fileline,cfgDict,row)
      elif (keyword == 'DATABASE'):
        parseDatabase(fileline,cfgDict,row)
      elif (keyword == 'WORKBOOK'):
        curWb = parseWorkbook(fileline,cfgDict,row)
      elif (keyword == 'WORKSHEET'):
        curWs = parseWorksheet(fileline,cfgDict,row,curWb)
      elif (keyword in ['MATRIX','SUMMARY','CHART']):
        parseObj(fileline,cfgDict,row,curWb,curWs)
      fileline += 1

  return cfgDict
