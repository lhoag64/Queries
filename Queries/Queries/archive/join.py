import logging
import sqlite3


def Join(db):

  c = db.cursor()

  c.execute \
    ( \
      '''
        SELECT 
          ts.fname,
          ts.lname,
          ts.region,
          ts.lbr_type,
          ts.prd_team,
          ts.fae_loc,
          ts.entry_date,
          ts.wbs_code,
          wbs.desc,
          wbs.downtime,
          wbs.leave,
          ts.work_loc,
          loc.desc,
          ts.activity,
          act.desc,
          act.billable,
          act.non_billable,
          act.pre_sales,
          ts.product,
          prd.desc,
          ts.hours,
          ts.work_type
        FROM timesheets AS ts
        INNER JOIN wbs_code AS wbs ON ts.wbs_code = wbs.code
        INNER JOIN location AS loc ON ts.work_loc = loc.location
        INNER JOIN activity AS act ON ts.activity = act.activity
        INNER JOIN product  AS prd ON ts.product  = prd.product
        WHERE region = 'EMEA'
        ORDER BY region,entry_date,lname,fname,wbs_code
      '''
    )

  wid = [( 8,'fname'),(12,'lname'),( 4,'rgn'),( 1,'pc'  ),( 3,'prd'  ),( 2,'loc'   ),(10,'date'), \
         ( 5,'code' ),(10,'cdesc'),( 1,'cdt'),( 1,'clv' ), \
         ( 3,'loc'  ),(10,'ldesc'),( 2,'act'),(10,'adsc'),( 1,'abill'),( 1,'anbill'),( 1,'apre'),\
         ( 2,'prd'  ),(10,'pdesc'),( 5,'hrs'),( 5,'lts' ),( 8,''     ),( 3,''      ),( 3,''    ),(3,''),(3,''),(3,'')]

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
  
  logging.debug('End of Program')

#  fae_lbrtype - key,desc
#  fae_loc - key,desc
#  fae_prdteam - key,desc
#  fae_region - key,desc
#  fae_team - fullname,fname,fnalias,lname,lnalias,region,lbr_type,prd_team,fae_loc,norm_hours,max_hours,start_date,end_date
#  wbs_code - code,desc,downtime,leave
#  location - location,desc
#  product - product,desc
#  activity - activity,desc,billable,pre_sales,non_billable
#  timesheets - name,fname,lname,region,lbr_type,prd_team,fae_loc,wc_date,entry_date,wbs_code,work_loc,activity,product,hours,work_type,notes,ts_name,ts_date,ts_file
#  work_type - key,desc
#  ts_file - file,desc