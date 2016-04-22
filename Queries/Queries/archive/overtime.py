import logging
import sqlite3


def Overtime(db):

  c = db.cursor()

  c.execute('SELECT wc_date FROM weeks ORDER BY wc_date')

  week = []
  for row in c.fetchall():
    week.append(row[0])

  region = 'EMEA'

  for i in range(1-1,13):

#    c.execute \
#      ( \
#        '''
#          SELECT ts.fname,ts.lname,fae.norm_hours,ts.wbs_code,ts.hours
#          FROM timesheets AS ts
#          INNER JOIN fae_team AS fae ON (ts.fname = fae.fname and ts.lname = fae.lname)
#          WHERE ts.region = ? and (ts.entry_date >= ? and ts.entry_date < ?)
#          GROUP BY fae.norm_hours
#        ''', (region,week[i],week[i+1]))
#
#    wid = [(8,'L','fname'),(12,'L','lname'),(6,'R','hours'),(5,'L','code'),(6,'R','hours')]

    c.execute \
      ( \
        '''
          SELECT sum(norm_hours) FROM fae_team WHERE region = ?
        ''', (region,))

    wid = [(6,'R','hours')]

    logging.debug('Week ' + str(i+1) + ' ' + week[i])
    for row in c.fetchall():
      index = 0
      text = '|'
      for col in row:
        w = wid[index][0]
        if (col is None):
          col = ''
        col = str(col)
        if (len(col) > w): col = col[:w]
        text += col.ljust(w) + '|'
        index += 1
      logging.debug(text)

    c.execute \
      ( \
        '''
          SELECT sum(hours) FROM timesheets
          WHERE region = ? and (entry_date >= ? and entry_date < ?)
        ''', (region,week[i],week[i+1]))

    wid = [(6,'R','hours')]

    logging.debug('Week ' + str(i+1) + ' ' + week[i])
    for row in c.fetchall():
      index = 0
      text = '|'
      for col in row:
        w = wid[index][0]
        if (col is None):
          col = ''
        col = str(col)
        if (len(col) > w): col = col[:w]
        text += col.ljust(w) + '|'
        index += 1
      logging.debug(text)

    logging.debug('')

#    c.execute \
#      ( \
#        '''
#          SELECT wbs.downtime,wbs.leave,sum(ts.hours)
#          FROM timesheets AS ts
#          INNER JOIN wbs_code AS wbs ON ts.wbs_code = wbs.code
#          WHERE region = ? and (ts.entry_date >= ? and ts.entry_date < ?)
#          GROUP BY wbs.downtime,wbs.leave
#        ''', (region,week[i],week[i+1]))
#
#    wid = [(1,'L','dt'),(1,'L','lv'),(6,'r','sum')]
#
#    logging.debug('Week ' + str(i+1) + ' ' + week[i])
#    for row in c.fetchall():
#      index = 0
#      text = '|'
#      for col in row:
#        w = wid[index][0]
#        if (col is None):
#          col = ''
#        col = str(col)
#        if (len(col) > w): col = col[:w]
#        text += col.ljust(w) + '|'
#        index += 1
#      logging.debug(text)
#
#    c.execute \
#      ( \
#        '''
#          SELECT sum(ts.hours)
#          FROM timesheets AS ts
#          WHERE region = ? and (ts.entry_date >= ? and ts.entry_date < ?)
#        ''', (region,week[i],week[i+1]))
#
#    wid = [(8,'L','fname'),(12,'L','lname'),(4,'L','act'),(1,'L','B'),(1,'L','P'),(6,'R','total')]
#
#    logging.debug('Week ' + str(i+1) + ' ' + week[i])
#    for row in c.fetchall():
#      index = 0
#      text = '|'
#      for col in row:
#        w = wid[index][0]
#        if (col is None):
#          col = ''
#        col = str(col)
#        if (len(col) > w): col = col[:w]
#        text += col.ljust(w) + '|'
#        index += 1
#      logging.debug(text)
#
#    logging.debug('')

#  timesheets - name,fname,lname,region,lbr_type,prd_team,fae_loc,wc_date,entry_date,wbs_code,work_loc,activity,product,hours,work_type,notes,ts_name,ts_date,ts_file
#  wbs_code - code,desc,downtime,leave
#  location - location,desc
#  product - product,desc
#  activity - activity,desc,billable,pre_sales,non_billable
#  work_type - key,desc
#  ts_file - file,desc
#  fae_lbrtype - key,desc
#  fae_loc - key,desc
#  fae_prdteam - key,desc
#  fae_region - key,desc
#  fae_team - fullname,fname,fnalias,lname,lnalias,region,lbr_type,prd_team,fae_loc,norm_hours,max_hours,start_date,end_date