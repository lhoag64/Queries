#import logging
#import sqlite3
#
##----------------------------------------------------------------------
#def GetFaeList(db,region,period):
#  c = db.cursor()
#
#  if (region == 'ALL'):
#    c.execute \
#      ( \
##        '''
#          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,fae.lbr_type
#          FROM fae_team AS fae
#          ORDER BY fae.lname,fae.fname
#        ''')
#  else:
#    c.execute \
#      ( \
#        '''
#          SELECT fae.fname,fae.lname,fae.norm_hours,fae.max_hours,fae.lbr_type
#          FROM fae_team AS fae
#          WHERE region = ?
#          ORDER BY fae.lname,fae.fname
#        ''',(region,))
#
#  faeList = c.fetchall()
#
#  result = []
#  for fae in faeList:
#    result.append([fae[0],fae[1],fae[2],fae[3],fae[4]])
#
#  return result
