import logging
import sqlite3


def LvT(db):

  c = db.cursor()

  c.execute('SELECT wc_date FROM weeks ORDER BY wc_date')

  week = []
  for row in c.fetchall():
    week.append(row[0])

  region = 'EMEA'

  for i in range(1-1,13):

    c.execute \
      ( \
        '''
          SELECT work_type, SUM(hours) AS total
          FROM timesheets AS ts
          WHERE region = ? and (ts.entry_date >= ? and ts.entry_date < ?)
          GROUP BY work_type
        ''', (region,week[i],week[i+1]))

    wid = [(4,'L','act'),(6,'R','total')]

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