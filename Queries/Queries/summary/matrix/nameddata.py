import logging

#----------------------------------------------------------------------
class NamedData:
  def __init__(self,tblName,name,rows,cols,srow,scol,data,tbl,keys):
    self.tblName = tblName
    self.rows    = rows
    self.cols    = cols
    self.sRow    = srow
    self.sCol    = scol
    self.data    = data
    self.tbl     = tbl
    self.keys    = keys
    self.name    = self.CreateName(tblName,name)

  def CreateName(self,tblName,dataName):

    #logging.debug('---------------------------------------------')
    #logging.debug(tblName)
    #logging.debug(dataName)
    #logging.debug(self.rows)
    #logging.debug(self.cols)

    rootName = ''
    for ch in tblName:
      if (ch.isalnum() != True):
        if (ch != '_' and ch != '.'):
          if (ch in ['[',']','(',')']):
            ch = ''
          else:
            if (ch == '-'):
              ch = '_'
            else:
              ch = '_'
      rootName += ch

    fullName = rootName

    stxt = dataName.split()
    for i in range(len(stxt)):
      stxt[i] = stxt[i].strip()
      if (stxt[i] == '-'):
        stxt[i] = ''
    dataName = ''
    for i in stxt:
      if (len(i) > 0):
        dataName += i + '_'
    dataName = dataName[:-1]

    name = ''
    for ch in dataName:
      if (ch == '%'):
        ch = 'PCT'
      elif (ch.isalnum() != True):
        if (ch != '_' and ch != '.'):
          if (ch in ['[',']','(',')','#',',']):
            ch = ''
          else:
            if (ch == '-'):
              ch = '_'
            else:
              ch = '_'
      name += ch

    prev = ''
    text = name
    name = ''
    for ch in text:
      if (ch == '_'):
        if (prev == '_'):
          ch = ''
        else:
          prev = ch
      elif (ch == '.'):
        if (prev == '.'):
          ch = ''
        else:
          prev = ch
      else:
        prev = ch
      name += ch

    fullName = fullName + '.-.' + name

    #logging.debug('---------------------------------------------')
    #cnt = len(fullName)
    #logging.debug(str(cnt).rjust(3) + ' | ' + fullName)
    #logging.debug('---------------------------------------------')

    return fullName