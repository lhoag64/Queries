import logging

#----------------------------------------------------------------------
class Fae:

  Regions      = [('AM','Americas'),('EMEA','Europe/Middle East'),('GC','Greater China'),('ROAPAC','Rest of APAC'),('BU','Business Unit')]
  ProductTeams = [('DMR','Digital Mobile Radio'),('MI','Modular Instruments'),('TVM','TeraVM'),('DAS','Coverage')]
  LaborTypes   = [('P','Direct Hire'),('C','Contractor')]
  Locatons     = [('N','North'),('S','South'),('E','East'),('W','West'),('R','Regional'), \
                  ('UK','United Kindom'),('SE','Sweden'),('FI','Finland'),('FR','France'),('DE','Germany')]

  def __init__(self,region,fname,fnalias,lname,lnalias,laborType,prodTeam,location,normHours,maxHours,startDate,endDate):
    self.region    = region
    self.fname     = fname
    self.fnalias   = fnalias
    self.lname     = lname
    self.lnalias   = lnalias
    self.lbrType   = laborType
    self.prdTeam   = prodTeam
    self.loc       = location
    self.normHours = normHours
    self.maxHours  = maxHours
    self.startDate = startDate
    self.endDate   = endDate

class FaeTeam:
  faes = None
  def __init__(self):
    faelist = []
    faelist.append(Fae('AM',  'Wray'    ,[       ],'Odom'        ,[                              ],'P','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Pankaj'  ,[       ],'Wadhwa'      ,[                              ],'C','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Kapil'   ,[       ],'Bhardwaj'    ,[                              ],'P','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Sohan'   ,[       ],'D\'souza'    ,['D\'Souza'                    ],'P','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Jeremy'  ,[       ],'Schroeder'   ,[                              ],'P','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Emad'    ,[       ],'Ramahi'      ,[                              ],'P','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Karun'   ,[       ],'Dua'         ,[                              ],'P','DMR','W' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Suarabh' ,[       ],'Dhancholia'  ,[                              ],'P','DMR','W' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Jeff'    ,[       ],'Smith'       ,[                              ],'P','DMR','W' ,40.0,60.0,'2014-01-01','2016-02-05'))
    faelist.append(Fae('AM',  'Paul'    ,[       ],'Khatkar'     ,[                              ],'P','DMR','W' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Joel'    ,[       ],'Joseph'      ,[                              ],'P','DMR','W' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Ashwini' ,[       ],'Bhagat'      ,[                              ],'P','DMR','W' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Jim'     ,[       ],'Morrison'    ,[                              ],'P','MI' ,'R' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Paul'    ,[       ],'Moser'       ,[                              ],'P','MI' ,'R' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Karl'    ,[       ],'Hornung'     ,[                              ],'P','MI' ,'R' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Jonathan',[       ],'Smith'       ,[                              ],'P','MI' ,'R' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Pouyan'  ,[       ],'Rostam'      ,[                              ],'C','DMR','C' ,40.0,60.0,'2014-01-01','2016-01-15'))
    faelist.append(Fae('AM',  'Karan'   ,[       ],'Kalsi'       ,[                              ],'C','DMR','C' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('AM',  'Pallavi' ,[       ],'Chaturvedi'  ,[                              ],'C','DMR','C' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Alex'    ,[       ],'Blackwood'   ,[                              ],'P','DMR','UK',37.5,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Piyush'  ,[       ],'Agarwal'     ,[                              ],'P','DMR','UK',37.5,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Jawid'   ,[       ],'Azizi'       ,[                              ],'P','DMR','UK',37.5,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Chu'     ,[       ],'Qi Yau'      ,['Yau'                         ],'P','DMR','UK',37.5,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Ashok'   ,[       ],'Yadav'       ,[                              ],'C','DMR','UK',37.5,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Haroon'  ,[       ],'Azizi'       ,[                              ],'P','DMR','UK',37.5,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Tomas'   ,[       ],'Helge'       ,[                              ],'C','DMR','SE',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Farshid' ,[       ],'Saidbahr'    ,[                              ],'P','DMR','SE',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Stefan'  ,[       ],'Edblom'      ,[                              ],'C','DMR','SE',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Rajesh'  ,[       ],'Kallingal'   ,[                              ],'C','DMR','SE',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Akash'   ,[       ],'Jha'         ,[                              ],'C','DMR','SE',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Joakim'  ,[       ],'Marjeta'     ,[                              ],'P','DMR','FI',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Kai'     ,[       ],'Hietala'     ,[                              ],'P','DMR','FI',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Jouni'   ,[       ],'Keski-Santti',[                              ],'C','DMR','FI',40.0,47.5,'2016-07-07','2020-01-01'))
    faelist.append(Fae('EMEA','Kamal'   ,[       ],'Mudgal'      ,[                              ],'C','DMR','FR',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Germain' ,[       ],'Irankunda'   ,['Irankanda'                   ],'C','DMR','FR',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('EMEA','Marco'   ,['Marko'],'Hofbeck'     ,[                              ],'P','DMR','DE',40.0,47.5,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Eric'    ,[       ],'Liu'         ,[                              ],'P','DMR','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Young'   ,[       ],'Wang'        ,[                              ],'P','DMR','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Ronald'  ,[       ],'Luan'        ,[                              ],'P','DMR','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Yukang'  ,[       ],'Tu'          ,[                              ],'P','DMR','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Wayne'   ,[       ],'Fu'          ,[                              ],'P','DMR','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Mark'    ,[       ],'Yan'         ,[                              ],'P','DMR','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Klein'   ,[       ],'Jiang'       ,[                              ],'P','DMR','S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Corey'   ,[       ],'Liu'         ,[                              ],'P','DMR','S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Huang'   ,[       ],'Wei'         ,[                              ],'P','DMR','S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Wang'    ,[       ],'Sining'      ,[                              ],'P','DMR','S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Iblic'   ,[       ],'Lin'         ,[                              ],'P','DMR','S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Tiger'   ,[       ],'Chen'        ,[                              ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Huang'   ,[       ],'Zheer'       ,[                              ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Gary'    ,[       ],'Wang'        ,[                              ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'David'   ,[       ],'Wang'        ,[                              ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Chien'   ,[       ],'Huang'       ,[                              ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Hu'      ,[       ],'Yu'          ,[                              ],'P','MI' ,'N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Eric'    ,[       ],'Wang'        ,[                              ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Kowski'  ,[       ],'Heieh'       ,['Hsieh'                       ],'P','MI' ,'S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Jun'     ,[       ],'Yang'        ,[                              ],'P','TVM','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Michael' ,[       ],'Zhang'       ,[                              ],'P','TVM','S' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Simon'   ,[       ],'Liu'         ,[                              ],'P','DAS','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Ray'     ,[       ],'Zhang'       ,[                              ],'P','DAS','N' ,40.0,60.0,'2014-01-01','2020-01-01'))
    faelist.append(Fae('GC'  ,'Zhao'    ,[       ],'Jing'        ,[                              ],'P','DAS','N' ,40.0,60.0,'2014-01-01','2016-02-01'))
    faelist.append(Fae('BU'  ,'Andy'    ,[       ],'Cooper'      ,[                              ],'P','DMR','E' ,40.0,60.0,'2014-01-01','2020-01-01'))

    self.faes = faelist