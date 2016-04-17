import logging
import sqlite3
from   logconfig        import LogConfig
from   activity         import Activity
from   createweekstable import CreateWeeksTable
from   lvt              import LvT
from   utilcf           import UtilizationCF

if (__name__ == '__main__'):
  LogConfig('queries.log')
  logging.debug('Start of Program')

  db = sqlite3.connect(r'X:\Reporting\Timesheets\timesheets.db')

  #CreateWeeksTable(db) 
  #Activity(db) 
  #LvT(db)
  UtilizationCF(db)

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