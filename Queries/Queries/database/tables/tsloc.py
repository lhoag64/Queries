import logging
import re
import sqlite3
from   database.tables.table import Table

LocDict =                                                                                        \
  {                                                                                              \
    113: [113, 1, 1,'EMEA'  ,'UK'                      ,'UK'      ,'UK'            ,'UK'         ,1,0,0,0],  \
    112: [112, 2, 2,'EMEA'  ,'Sweden'                  ,'SE'      ,'Sweden'        ,'SE'         ,1,0,0,0],  \
    101: [101, 3, 3,'EMEA'  ,'Finland'                 ,'FI'      ,'Finland'       ,'FI'         ,1,0,0,0],  \
    102: [102, 4, 4,'EMEA'  ,'France'                  ,'FR'      ,'France'        ,'FR'         ,1,0,0,0],  \
    103: [103, 5, 5,'EMEA'  ,'Germany'                 ,'DE'      ,'Germany'       ,'DE'         ,1,0,0,0],  \
    105: [105, 6, 6,'EMEA'  ,'Israel'                  ,'IS'      ,'Israel'        ,'IS'         ,0,0,0,0],  \
    109: [109, 7, 6,'EMEA'  ,'Poland'                  ,'PL'      ,'Poland'        ,'PL'         ,0,0,0,0],  \
    110: [110, 8, 6,'EMEA'  ,'Portugal'                ,'PT'      ,'Portugal'      ,'PT'         ,0,0,0,0],  \
    111: [111, 9, 6,'EMEA'  ,'Spain'                   ,'SP'      ,'Spain'         ,'SP'         ,0,0,0,0],  \
    130: [130,10, 6,'EMEA'  ,'Ireland'                 ,'IR'      ,'Ireland'       ,'IR'         ,0,0,0,0],  \
    131: [131,11, 6,'EMEA'  ,'Turkey'                  ,'TR'      ,'Turkey'        ,'TR'         ,0,0,0,0],  \
    100: [100, 3, 9,'GC'    ,'Greater China'           ,'GC'      ,'China'         ,'GC'         ,0,0,1,0],  \
    115: [115, 1,10,'AM'    ,'AM-NorthEast'            ,'US-NE'   ,'US-NorthEast'  ,'US-EAST'    ,0,1,0,0],  \
    116: [116, 2,10,'AM'    ,'AM-MidAtlantic'          ,'US-CE'   ,'US-MidAtlantic','US-EAST'    ,0,1,0,0],  \
    117: [117, 3,10,'AM'    ,'AM-SouthEast'            ,'US-SE'   ,'US-SouthEast'  ,'US-EAST'    ,0,1,0,0],  \
    118: [118, 4,10,'AM'    ,'AM-NorthPlains'          ,'US-NC'   ,'US-NorthCental','US-EAST'    ,0,1,0,0],  \
    119: [119, 5,10,'AM'    ,'AM-SouthPlains'          ,'US-SC'   ,'US-SouthCental','US-EAST'    ,0,1,0,0],  \
    120: [120, 6,11,'AM'    ,'AM-NorthWest'            ,'US-NW'   ,'US-NorthWest'  ,'US-WEST'    ,0,1,0,0],  \
    121: [121, 7,11,'AM'    ,'AM-SouthWest'            ,'US-SW'   ,'US-SouthWest'  ,'US-WEST'    ,0,1,0,0],  \
    122: [122, 8,11,'AM'    ,'AM-Southern California'  ,'US-SD'   ,'US-SoCal'      ,'US-WEST'    ,0,1,0,0],  \
    123: [123, 9,11,'AM'    ,'AM-Bay Area'             ,'US-BA'   ,'US-BayArea'    ,'US-WEST'    ,0,1,0,0],  \
    124: [124,10,12,'AM'    ,'AM-Canada East'          ,'CA-E'    ,'CA-East'       ,'CA'         ,0,1,0,0],  \
    125: [125,11,13,'AM'    ,'AM-Canada West'          ,'CA-W'    ,'CA-West'       ,'CA'         ,0,0,0,0],  \
    126: [126,12,13,'AM'    ,'AM-Latin America'        ,'LS'      ,'LA'            ,'LA'         ,0,0,0,0],  \
    127: [127,13,13,'AM'    ,'AM-South America'        ,'SA'      ,'SA'            ,'SA'         ,0,0,0,0],  \
    114: [114,14,13,'AM'    ,'US'                      ,'US'      ,'US'            ,'US-REGIONAL',0,0,0,0],  \
    104: [104, 1,15,'ROAPAC','India'                   ,'IN'      ,'India'         ,'IN'         ,0,0,0,1],  \
    106: [106, 2,15,'ROAPAC','Japan'                   ,'JP'      ,'Japan'         ,'JP'         ,0,0,0,1],  \
    107: [107, 3,15,'ROAPAC','Korea'                   ,'KO'      ,'Korea'         ,'KO'         ,0,0,0,1],  \
    129: [129, 4,16,'ROAPAC','Malaysia'                ,'MA'      ,'Malaysia'      ,'MA'         ,0,0,0,0],  \
    108: [108, 5,16,'ROAPAC','Singapore'               ,'SI'      ,'Singapore'     ,'SI'         ,0,0,0,0],  \
    128: [128, 1, 1,'GLOBAL','Other'                   ,'OTH'     ,'OTH'           ,'OTH'        ,0,0,0,0]   \
  }

#----------------------------------------------------------------------
class TsLocTable(Table):
  def __init__(self):
    pass

  def Create(self,db,list):

    c = db.cursor()

    try:
      c.execute('DROP TABLE ts_loc')
    except sqlite3.OperationalError:
      pass

    c.execute \
      ( \
        '''
           CREATE TABLE ts_loc
             (
               loc          INTEGER UNIQUE PRIMARY KEY,
               loc_order    INTEGER,
               loc_group    INTEGER,
               region       TEXT,
               desc         TEXT,
               short_desc   TEXT,
               rgn_desc     TEXT,
               rgn_loc      TEXT,
               emea_key     INTEGER,
               am_key       INTEGER,
               gc_key       INTEGER,
               apac_key     INTEGER
             )
        '''
      )

    locations = set([])
    decodedRows = []
    for item in list:
      matches = []
      for match in re.finditer('[-|–]',item):
        matches.append((match.start(),match.end()))
      if (len(matches) == 0):
        logging.error('Can\'t find \'-\' in Code string:\'' + item + '\'')
        continue
      loc      = matches[-1]
      location = int(item[loc[1]:].strip())
      desc     = item[:loc[0]].strip()

      if (location not in locations):
        locations.add(location)
      else:
        logging.error('Location is already used:\'' + item + '\',skipping')
        continue

      row = (location,desc)
      decodedRows.append(row)

    rows = []
    for row in decodedRows:
      if (row[0] in LocDict):
        tup = tuple(LocDict[row[0]])
        if (row[0] != tup[0]):
          raise
      else:
        logging.error('Error finding location: ' + str(row[0]) + ' ' + row[1])
        raise

      rows.append(tup)

    c.executemany('INSERT INTO ts_loc VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',rows)

    db.commit()



