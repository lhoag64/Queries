import logging
import datetime
import re
import sqlite3
from   database.tables.table import Table

#----------------------------------------------------------------------
class TsEntryTable(Table):
  def __init__(self):
    pass

  #--------------------------------------------------------------------
  def getWeDate(self,wc):
    stxt = wc.split('-')
    wcDate = datetime.date(int(stxt[0]),int(stxt[1]),int(stxt[2]))
    weDate = wcDate + datetime.timedelta(days=6)
    weDate = weDate.strftime('%Y-%m-%d')
    return weDate

  #--------------------------------------------------------------------
  def Create(self,db):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_entry')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_entry
             (
               fname       TEXT,
               lname       TEXT,
               region      TEXT,
               lbr_type    TEXT,
               prd_team    TEXT,
               fae_loc     TEXT,
               wc_date     TEXT,
               entry_date  TEXT,
               wbs_code    TEXT,
               work_loc    TEXT,
               activity    TEXT,
               product     TEXT,
               hours       NUMERIC,
               work_type   TEXT,
               notes       TEXT,
               ts_name     TEXT,
               ts_date     TEXT,
               ts_file     TEXT,
               FOREIGN KEY (region) REFERENCES fae_region(key),
               FOREIGN KEY (lbr_type) REFERENCES fae_lbrtype(key),
               FOREIGN KEY (prd_team) REFERENCES fae_prdteam(key),
               FOREIGN KEY (fae_loc) REFERENCES fae_loc(key),
               FOREIGN KEY (work_type) REFERENCES work_type(key)
               FOREIGN KEY (ts_file) REFERENCES ts_files(key)
             )
        '''
      )

    db.commit()

  #--------------------------------------------------------------------
  def Insert(self,db,tsdata):
    check = {}
    c = db.cursor()
    c.execute('SELECT * FROM ts_code')
    check['CODE'] = {}
    for val in c.fetchall():
      check['CODE'][val[0]] = (val[0],val[1])

    c.execute('SELECT * FROM ts_act')
    check['ACT'] = {}
    for val in c.fetchall():
      check['ACT'][val[0]] = (val[0],val[1])

    c.execute('SELECT * FROM ts_loc')
    check['LOC'] = {}
    for val in c.fetchall():
      check['LOC'][val[0]] = (val[0],val[4])

    c.execute('SELECT * FROM ts_prd')
    check['PRD'] = {}
    for val in c.fetchall():
      check['PRD'][val[0]] = (val[0],val[1])

    dict = tsdata.tsdict

    entries = [] 
    for week in dict:
      for ts in dict[week]:  
        for entry in ts.entries:
          entries.append(self.generateEntry(db,tsdata.region,ts,entry,check))

    c.executemany('INSERT INTO ts_entry VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',entries)
    db.commit()

  #--------------------------------------------------------------------
  def generateEntry(self,db,region,ts,entry,check):

    #--------------------------------------------------------------------
    # Clean codes and verify
    #--------------------------------------------------------------------
    code = ''
    if (len(entry.code) > 0):
      matches = []
      for match in re.finditer('[-|–]',entry.code):
        matches.append((match.start(),match.end()))
      if (len(matches) < 1):
        logging.error('Invalid Code: ' + entry.code)
      else:
        hyphen = matches[-1]
        code      = str(entry.code[hyphen[1]:].strip())
        code_desc = str(entry.code[:hyphen[0]].strip())

        if (code not in check['CODE']):
          logging.warn('Invalid Code in timesheet: ' + code + ' ' + entry.tsfile)
        else:
          pass

    #--------------------------------------------------------------------
    # Clean activity and verify
    #--------------------------------------------------------------------
    act = ''
    if (len(entry.activity) > 0):
      matches = []
      for match in re.finditer('-',entry.activity):
        matches.append((match.start(),match.end()))
      if (len(matches) < 1):
        logging.error('Invalid Activity: ' + entry.activity)
      else:
        hyphen = matches[-1]
        act       = int(entry.activity[hyphen[1]:].strip())
        act_desc  = str(entry.activity[:hyphen[0]].strip())
  
        if (act not in check['ACT']):
          logging.warn('Invalid Activity in timesheet: ' +  str(act) + ' ' + entry.tsfile)
        else:
          if (act_desc.upper() != check['ACT'][act][1].upper()): 
            logging.warn('Activty and activity description don\'t match: ' + str(act) + ' ' + act_desc + ' ' + check['ACT'][act][1])
            found = False
            for item in check['ACT']:
              if (act_desc.upper() == check['ACT'][item][1].upper()):
                found = True
                act = int(item)
                logging.warn('Changed to: ' + str(act) + ' ' + check['ACT'][act][1])
                break
            if (not found):
              logging.warn('Activity code mismatch: ' + str(act) + ' ' + act_desc + ' ' + check['ACT'][act][1])
  
    #--------------------------------------------------------------------
    # Clean location and verify
    #--------------------------------------------------------------------
    loc = ''
    if (len(entry.location) > 0):
      matches = []
      for match in re.finditer('-',entry.location):
        matches.append((match.start(),match.end()))
      if (len(matches) < 1):
        logging.error('Invalid Location: ' + entry.location)
      else:
        hyphen = matches[-1]
        loc       = int(entry.location[hyphen[1]:].strip())
        loc_desc  = str(entry.location[:hyphen[0]].strip())
  
        if (loc not in check['LOC']):
          logging.warn('Invalid Location in timesheet: ' +  str(loc) + ' ' + entry.tsfile)
        else:
          if (loc_desc.upper() != check['LOC'][loc][1].upper()): 
            logging.warn('Location and location description don\'t match: ' + str(loc) + ' ' + loc_desc + ' ' + check['LOC'][loc][1])
            found = False
            for item in check['LOC']:
              if (loc_desc.upper() == check['LOC'][item][1].upper()):
                found = True
                loc = int(item)
                logging.warn('Changed to: ' + str(loc) + ' ' + check['LOC'][loc][1])
                break
            if (not found):
              logging.warn('Location code mismatch: ' + str(loc) + ' ' + loc_desc + ' ' + check['LOC'][loc][1])
             
    #--------------------------------------------------------------------
    # Clean product and verify
    #--------------------------------------------------------------------
    prd = ''
    if (len(entry.product) > 0):
      matches = []
      for match in re.finditer('-',entry.product):
        matches.append((match.start(),match.end()))
      if (len(matches) < 1):
        logging.error('Invalid Product: ' + entry.product)
      else:
        hyphen = matches[-1]
        prd       = int(entry.product[hyphen[1]:].strip())
        prd_desc  = str(entry.product[:hyphen[0]].strip())
  
        if (prd not in check['PRD']):
          logging.warn('Invalid Product in timesheet: ' +  prd + ' ' + entry.tsfile)
        else:
          if (prd_desc.upper() != check['PRD'][prd][1].upper()): 
            logging.warn('Product and product description don\'t match: ' + str(prd) + ' ' + prd_desc + ' ' + check['PRD'][prd][1])
            found = False
            for item in check['PRD']:
              if (prd_desc.upper() == check['PRD'][item][1].upper()):
                found = True
                prd = int(item)
                logging.warn('Changed to: ' + str(prd) + ' ' + check['PRD'][prd][1])
                break
            if (not found):
              logging.warn('Product code mismatch: ' + str(prd) + ' ' + prd_desc + ' ' + check['PRD'][prd][1])
              prd = None
  
    #--------------------------------------------------------------------
    # Clean up workType if possible
    #--------------------------------------------------------------------
    wt = ''
    if (len(entry.workType) == 0):
      if (len(code) == 5 and code[0:1] == 'X'):
        wt = 'Labour'
    else:
      wt = entry.workType
  
    #--------------------------------------------------------------------
    # Clean up for X codes
    #--------------------------------------------------------------------
    if (len(code) == 5 and code[0:1] == 'X'):
      if (loc is not None):
        logging.warn('Location has value for : ' + code + ' correcting')
        loc = None
      if (act is not None):
        logging.warn('Activity has value for : ' + code + ' correcting')
        act = None
      if (prd is not None):
        logging.warn('Product has value for : ' + code + ' correcting')
        prd = None
  
    fname     = ts.tsInfo.fname
    lname     = ts.tsInfo.lname
    rgn       = region
    lbrType   = ts.tsInfo.fae.lbrType
    prdTeam   = ts.tsInfo.fae.prdTeam
    faeLoc    = ts.tsInfo.fae.location
    wcDate    = str(ts.tsInfo.wsDate)
    entryDate = str(entry.date)
    wbsCode   = code
    workLoc   = loc
    activity  = act
    product   = prd
    hours     = entry.hours
    workType  = wt
    note      = entry.note
    tsName    = entry.tsname
    tsDate    = entry.tsdate
    tsFile    = entry.tsfile
  
    result =                                                                     \
      (fname,lname,rgn,lbrType,prdTeam,faeLoc,wcDate,entryDate,                  \
       wbsCode,workLoc,activity,product,hours,workType,note,tsName,tsDate,tsFile)
  
    return result


