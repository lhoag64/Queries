import os.path
import logging
import sqlite3
from   database.tsdatabase import TsDatabase as TsDb

#----------------------------------------------------------------------
class Database:
  def __init__(self):
    Database.tsdb = TsDb()
    Database.db   = None

  #--------------------------------------------------------------------
  def GetDb():
    return Database.db

  #--------------------------------------------------------------------
  def Connect(root,dbname):
    Database.db = Database.tsdb.Connect(root,dbname)

  #--------------------------------------------------------------------
  def CreateTables(list):
    Database.tsdb.CreateTables(list)

  #--------------------------------------------------------------------
  def InsertTimesheets(tsdata):
    Database.tsdb.InsertTimesheets(tsdata)

  #--------------------------------------------------------------------
  def GetWeeks(period):
    return Database.tsdb.GetWeeks(period)

  #--------------------------------------------------------------------
  def GetActivities(type):
    return Database.tsdb.GetActivities(type)

  #--------------------------------------------------------------------
  def GetActivitySum(region,act,period):
    return Database.tsdb.GetActivitySum(region,act,period)

  #--------------------------------------------------------------------
  def GetLts(type):
    return Database.tsdb.GetLts(type)

  #--------------------------------------------------------------------
  def GetLtsSum(region,lts,period):
    return Database.tsdb.GetLtsSum(region,lts,period)

  #--------------------------------------------------------------------
  def GetUtlCfSum(region,period):
    return Database.tsdb.GetUtlCfSum(region,period)

  #--------------------------------------------------------------------
  def GetUtlPsSum(region,period):
    return Database.tsdb.GetUtlPsSum(region,period)

  #--------------------------------------------------------------------
  def GetUtlDtSum(region,period):
    return Database.tsdb.GetUtlDtSum(region,period)

  #--------------------------------------------------------------------
  def GetUtlLsSum(region,period):
    return Database.tsdb.GetUtlLsSum(region,period)
  
  #--------------------------------------------------------------------
  def GetOverTimeSum(region,period):
    return Database.tsdb.GetOverTimeSum(region,period)

  #-------------------------------------------------------------------- 
  def GetGkaSum(region,codes,period):
    return Database.tsdb.GetGkaSum(region,codes,period)

  #--------------------------------------------------------------------
  def GetActByLocSum(region,act,loc,period):
    return Database.tsdb.GetActByLocSum(region,act,loc,period)

  #--------------------------------------------------------------------
  def GetFaeAwhSum(region,period):
    return Database.tsdb.GetFaeAwhSum(region,period)





