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
      check['LOC'][val[0]] = (val[0],val[1])

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
  def GetActivitySum(self,db,region,act,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT activity, SUM(hours) AS total
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY activity
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT activity, SUM(hours) AS total
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY activity
            ''',(region,wcDate,weDate))

      resultList = c.fetchall()
      resultDict = {}
      for result in resultList:
        if (result[0] and len(result[0]) > 0):
          resultDict[int(result[0])] = result[1]

      data = []
      for item in act:
        if (item[0] in resultDict):
          data.append(float(resultDict[item[0]]))
        else:
          data.append(0.0)

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetLtsSum(self,db,region,lts,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT work_type, SUM(hours) AS total
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY work_type
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT work_type, SUM(hours) AS total
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY work_type
            ''',(region,wcDate,weDate))

      resultList = c.fetchall()
      resultDict = {}
      for result in resultList:
        if (result[0] and len(result[0]) > 0):
          resultDict[result[0]] = result[1]

      data = []
      for item in lts:
        if (item[0] in resultDict):
          data.append(float(resultDict[item[0]]))
        else:
          data.append(0.0)

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetUtlCfSum(self,db,region,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT act.billable,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_act AS act ON ts.activity = act.act
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY act.billable
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT act.billable,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_act AS act ON ts.activity = act.act
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY act.billable
            ''',(region,wcDate,weDate))

      utlList = c.fetchall()

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(region,wcDate,weDate))

      totList = c.fetchall()

      billable = 0.0
      for item in utlList:
        if (item[0] == 1):
          billable = item[1]
          break

      if (len(utlList) > 0):
        data = [billable,totList[0][0],billable/totList[0][0] * 100.0]
      else:
        data = [0.0,0.0,0.0]
      #logging.debug(str(data[0]).rjust(5) + ' ' + str(data[1]).rjust(5))

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetUtlPsSum(self,db,region,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT act.pre_sales,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_act AS act ON ts.activity = act.act
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY act.billable
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT act.pre_sales,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_act AS act ON ts.activity = act.act
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY act.billable
            ''',(region,wcDate,weDate))

      utlList = c.fetchall()

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(region,wcDate,weDate))

      totList = c.fetchall()

      presale = 0.0
      for item in utlList:
        if (item[0] == 1):
          presale = item[1]
          break

      if (len(utlList) > 0):
        data = [presale,totList[0][0],presale/totList[0][0] * 100.0]
      else:
        data = [0.0,0.0,0.0]

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetUtlDtSum(self,db,region,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.downtime = 1)
              GROUP BY wbs.code
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.downtime = 1)
              GROUP BY wbs.code
            ''',(region,wcDate,weDate))

      utlList = c.fetchall()

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(region,wcDate,weDate))

      totList = c.fetchall()

      if (len(utlList) > 0):
        sum = 0.0
        for item in utlList:
          sum += item[3]
        tot = totList[0][0]
        data = [sum,tot,sum/tot * 100.0]
      else:
        data = [0.0,0.0,0.0]
      #logging.debug(str(data[0]).rjust(5) + ' ' + str(data[1]).rjust(5))

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetUtlLsSum(self,db,region,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.leave = 1)
              GROUP BY wbs.code
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT wbs.code,wbs.downtime,wbs.leave,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and (wbs.leave = 1)
              GROUP BY wbs.code
            ''',(region,wcDate,weDate))

      utlList = c.fetchall()

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT sum(ts.hours)
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(region,wcDate,weDate))

      totList = c.fetchall()

      if (len(utlList) > 0):
        sum = 0.0
        for item in utlList:
          sum += item[3]
        tot = totList[0][0]
        data = [sum,tot,sum/tot * 100.0]
      else:
        data = [0.0,0.0,0.0]

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetOverTimeSum(self,db,region,weeks):

    c = db.cursor()
    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT sum(norm_hours) FROM fae_team
            ''')
      else:
        c.execute \
          ( \
            '''
            SELECT sum(norm_hours) FROM fae_team WHERE region = ?
            ''',(region,))

      nrmList = c.fetchall()

      if (region == 'ALL'):
        c.execute \
        ( \
            '''
              SELECT sum(hours)
              FROM ts_entry AS ts
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(wcDate,weDate))
      else:
        c.execute \
        ( \
            '''
              SELECT sum(hours)
              FROM ts_entry AS ts
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
            ''',(region,wcDate,weDate))

      totList = c.fetchall()

      if (totList[0][0]):
        nrm = nrmList[0][0]
        tot = totList[0][0]
        ot  = tot - nrm
        data = [ot,nrm,ot/tot * 100.0]
      else:
        data = [0.0,0.0,0.0]
      #logging.debug(str(data[0]).rjust(5) + ' ' + str(data[1]).rjust(5))

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetGkaSum(self,db,region,codes,weeks):

    c = db.cursor()
    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT wbs.code,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and 
                (wbs.gkacct = 1 or wbs.code = 'TTT' or wbs_code = 'COB' or wbs_code = 'OTH')
              GROUP BY wbs.code
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT wbs.code,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and 
                (wbs.gkacct = 1 or wbs.code = 'TTT' or wbs_code = 'COB' or wbs_code = 'OTH')
              GROUP BY wbs.code
            ''',(region,wcDate,weDate))

      codesList = c.fetchall()
      codesDict = {}
      for code in codesList:
        if (code[0] and len(code[0]) > 0):
          if (code[0] == 'NSN'):
            if ('NOK' in codesDict):
              codesDict['NOK'] += code[1]
          else:
            codesDict[code[0]] = code[1]

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT wbs.code,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and 
                (wbs.gkacct = 0 and wbs.code <> 'TTT' and wbs_code <> 'COB' and wbs_code <> 'OTH')
              GROUP BY wbs.code
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT wbs.code,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_code AS wbs ON ts.wbs_code = wbs.code
              WHERE region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and 
                (wbs.gkacct = 0 and wbs.code <> 'TTT' and wbs_code <> 'COB' and wbs_code <> 'OTH')
              GROUP BY wbs.code
            ''',(region,wcDate,weDate))
      
      otherList = c.fetchall()
      otherSum = 0.0
      for item in otherList:
        code = item[0]
        hrs  = item[1]
        if (len(code) == 3):
          otherSum += hrs

      codesDict['OTHERS'] = otherSum

      data = []
      for item in codes:
        if (item in codesDict):
          data.append(float(codesDict[item]))
        else:
          data.append(0.0)

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetActByLocSum(self,db,region,act,loc,weeks):

    locSet = set([])
    for item in loc:
      locSet.add(item)

    c = db.cursor()
    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT ts.activity,loc.loc,loc.desc,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_loc AS loc ON ts.work_loc = loc.loc
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
              GROUP BY ts.work_loc
            ''',(wcDate,weDate,act))
      else:
        c.execute \
          ( \
            '''
              SELECT ts.activity,loc.loc,loc.desc,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN ts_loc AS loc ON ts.work_loc = loc.loc
              WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and ts.activity = ?
              GROUP BY ts.work_loc
            ''',(region,wcDate,weDate,act))

      resultList = c.fetchall()
      resultDict = {}
      resultDict['Other (EMEA)'] = 0
      for result in resultList:
        if (result[0] and len(result[0]) > 0):
          if (result[2] in locSet):
            resultDict[result[2]] = result[3]
          else:
            resultDict['Other (EMEA)'] += result[3]

      data = []
      for item in loc:
        if (item in resultDict):
          data.append(float(resultDict[item]))
        else:
          data.append(0.0)

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetFaeList(self,db,region,weeks):
    c = db.cursor()

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,fae.lbr_type
            FROM fae_team AS fae
            ORDER BY fae.lname,fae.fname
          ''')
    else:
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,fae.lbr_type
            FROM fae_team AS fae
            WHERE region = ?
            ORDER BY fae.lname,fae.fname
          ''',(region,))

    faeList = c.fetchall()

    result = []
    for fae in faeList:
      result.append([fae[0],fae[1],fae[2],fae[3],fae[4]])

    return result

 #--------------------------------------------------------------------
  def GetFaeAwhSum(self,db,region,weeks):

    c = db.cursor()

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
            FROM fae_team AS fae
            ORDER BY fae.lname,fae.fname
          ''')
    else:
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
            FROM fae_team AS fae
            WHERE region = ?
            ORDER BY fae.lname,fae.fname
          ''',(region,))

    faes = c.fetchall()
    faeList = []
    faeDict = {}
    for fae in faes:
      faeList.append((fae[0],fae[1]))
      faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4])

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
              GROUP BY ts.fname,ts.lname
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
              GROUP BY ts.fname,ts.lname
            ''',(region,wcDate,weDate))

      hoursList = c.fetchall()
      hoursDict = {}
      for fae in hoursList:
        if ((fae[0],fae[1]) not in hoursDict):
          hoursDict[(fae[0],fae[1])] = float(fae[2])
        else:
          logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

      data = []
      for fae in faeList:
        if ((fae[0],fae[1]) in hoursDict):
          actHours = float(hoursDict[(fae[0],fae[1])])
          data.append((fae[0],fae[1],actHours))
        else:
          data.append((fae[0],fae[1],0.0))

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetFaeOtSum(self,db,region,weeks):

    c = db.cursor()

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
            FROM fae_team AS fae
            ORDER BY fae.lname,fae.fname
          ''')
    else:
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
            FROM fae_team AS fae
            WHERE region = ?
            ORDER BY fae.lname,fae.fname
          ''',(region,))

    faes = c.fetchall()
    faeList = []
    faeDict = {}
    for fae in faes:
      faeList.append((fae[0],fae[1]))
      faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4])

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,wbs.leave,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY ts.fname,ts.lname,wbs.leave
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,wbs.leave,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY ts.fname,ts.lname,wbs.leave
            ''',(region,wcDate,weDate))

      hoursList = c.fetchall()
      resultSet = set([])
      wkHrsDict = {}
      for fae in hoursList:
        resultSet.add((fae[0],fae[1]))
        if ((fae[0],fae[1]) not in wkHrsDict):
          if (fae[2] == 0):
            wkHrsDict[(fae[0],fae[1])] = float(fae[3])
        else:
          if (fae[2] != 1):
            logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

      lvHrsDict = {}
      for fae in hoursList:
        if ((fae[0],fae[1]) not in lvHrsDict):
          if (fae[2] == 1):
            lvHrsDict[(fae[0],fae[1])] = float(fae[3])
        else:
          if (fae[2] != 0):
            logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

      data = []
      for fae in faeList:
        wkHours = 0.0
        lvHours = 0.0
        if ((fae[0],fae[1]) in wkHrsDict):
          wkHours = float(wkHrsDict[(fae[0],fae[1])])
        if ((fae[0],fae[1]) in lvHrsDict):
          lvHours = float(lvHrsDict[(fae[0],fae[1])])
        if ((fae[0],fae[1]) in resultSet):
          data.append((fae[0],fae[1],wkHours,lvHours))
        else:
          lvHrs = float(faeDict[(fae[0],fae[1])][0])
          data.append((fae[0],fae[1],0.0,lvHrs))

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetFaeWhSum(self,db,region,weeks):

    c = db.cursor()

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
            FROM fae_team AS fae
            ORDER BY fae.lname,fae.fname
          ''')
    else:
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type
            FROM fae_team AS fae
            WHERE region = ?
            ORDER BY fae.lname,fae.fname
          ''',(region,))

    faes = c.fetchall()
    faeList = []
    faeDict = {}
    for fae in faes:
      faeList.append((fae[0],fae[1]))
      faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4])

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY ts.fname,ts.lname
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY ts.fname,ts.lname
            ''',(region,wcDate,weDate))

      hoursList = c.fetchall()
      hoursDict = {}
      for fae in hoursList:
        if ((fae[0],fae[1]) not in hoursDict):
          hoursDict[(fae[0],fae[1])] = float(fae[2])
        else:
          logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

      data = []
      for fae in faeList:
        if ((fae[0],fae[1]) in hoursDict):
          actHours = float(hoursDict[(fae[0],fae[1])])
          data.append((fae[0],fae[1],actHours))
        else:
          data.append((fae[0],fae[1],0.0))

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetFaeLtSum(self,db,region,weeks):

    c = db.cursor()

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT fae.lbr_type,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY fae.lbr_type
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT fae.lbr_type,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?)
              GROUP BY fae.lbr_type
            ''',(region,wcDate,weDate))

      hoursList = c.fetchall()
      hoursDict = {}
      for item in hoursList:
        if (item[0] not in hoursDict):
          hoursDict[item[0]] = item[1]

      data = []
      for item in ['P','C']:
        if (item in hoursDict):
          data.append(float(hoursDict[item]))
        else:
          data.append(0.0)

      weekList.append(data)

    return weekList

 #--------------------------------------------------------------------
  def GetFaeHourSummary(self,db,region,weeks):

    c = db.cursor()

    if (region == 'ALL'):
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type,region
            FROM fae_team AS fae
            ORDER BY fae.region,fae.lname,fae.fname
          ''')
    else:
      c.execute \
        ( \
          '''
            SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,lbr_type,region
            FROM fae_team AS fae
            WHERE region = ?
            ORDER BY fae.region,fae.lname,fae.fname
          ''',(region,))

    faes = c.fetchall()
    faeList = []
    faeDict = {}
    for fae in faes:
      faeList.append((fae[0],fae[1]))
      faeDict[(fae[0],fae[1])] = (fae[2],fae[3],fae[4],fae[5])

    weekList = []
    for i in range(len(weeks)):

      wcDate = weeks[i][0]
      weDate = self.getWeDate(wcDate)

      if (region == 'ALL'):
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
              GROUP BY ts.fname,ts.lname
            ''',(wcDate,weDate))
      else:
        c.execute \
          ( \
            '''
              SELECT ts.fname,ts.lname,sum(ts.hours)
              FROM ts_entry AS ts
              INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
              INNER JOIN ts_code  AS wbs ON (ts.wbs_code = wbs.code)
              WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date <= ?) and wbs.leave = 0
              GROUP BY ts.fname,ts.lname
            ''',(region,wcDate,weDate))

      hoursList = c.fetchall()
      hoursDict = {}
      for fae in hoursList:
        if ((fae[0],fae[1]) not in hoursDict):
          hoursDict[(fae[0],fae[1])] = float(fae[2])
        else:
          logging.error('Duplicate name in query results: ' + fae[0] + ' ' + fae[1])

      data = []
      for fae in faeList:
        if ((fae[0],fae[1]) in hoursDict):
          actHours = float(hoursDict[(fae[0],fae[1])])
          data.append((fae[0],fae[1],actHours))
        else:
          data.append((fae[0],fae[1],0.0))

      weekList.append(data)

    faeAvgDict = {}
    for week in weekList:
      for fae in week:
        t = (fae[0],fae[1])
        if (t not in faeAvgDict):
          faeAvgDict[t] = {}
          faeAvgDict[t]['SUM'] = 0.0
          faeAvgDict[t]['CNT'] =   0
          faeAvgDict[t]['NRM'] = float(faeDict[t][0])
          faeAvgDict[t]['MAX'] = float(faeDict[t][1])
          faeAvgDict[t]['LBR'] = faeDict[t][2]
          faeAvgDict[t]['RGN'] = faeDict[t][3]
        faeAvgDict[t]['SUM'] += float(fae[2])
        faeAvgDict[t]['CNT'] += 1

    result = []
    for fae in faeList:
      t = (fae[0],fae[1])
      sum = faeAvgDict[t]['SUM']
      cnt = faeAvgDict[t]['CNT']
      nrm = faeAvgDict[t]['NRM']
      max = faeAvgDict[t]['MAX']
      lbr = faeAvgDict[t]['LBR']
      rgn = faeAvgDict[t]['RGN']
      avg = sum/float(cnt)
      ot  = avg - nrm
      name = fae[0] + ' ' + fae[1]
      result.append((name,avg,ot,nrm,max,lbr,rgn))

    return result


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


