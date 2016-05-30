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
    self.name    = NamedData.CreateName(tblName,name)

  #--------------------------------------------------------------------
  class NamePath:
    def __init__(self,name):
      self.wsName   = None
      self.type     = None
      self.region   = None
      self.period   = None
      self.objName  = None
      self.itemList = None
      self.itemType = None

      foundDash = False
      itemList = []
      while (len(name) > 0):
        cIdx = 0
        for ch in name:
          if (ch == '.'):
            break
          if ((cIdx > 0) and (cIdx < len(name))):
            p = name[cIdx-1]
            c = name[cIdx+0]
            n = name[cIdx+1]
            if (p == '.' and c == 'X' and n == '.'):
              foundDash = True
              break
          cIdx += 1
        if (len(name[:cIdx]) > 0):
          itemList.append(name[:cIdx])
        cIdx += 1
        name = name[cIdx:]
        if (foundDash):
          break

      self.wsName  = itemList[0]
      self.type    = itemList[1]
      self.region  = itemList[2]
      self.period  = itemList[3]
      itemList = itemList[4:]
      self.objName = '.'.join(itemList)

      if (foundDash):
        name = name[cIdx:]
        itemList = []
        while (len(name) > 0):
          cIdx = 0
          for ch in name:
            if (ch == '.'):
              break
            cIdx += 1
          if (len(name[:cIdx]) > 0):
            itemList.append(name[:cIdx])
          cIdx += 1
          name = name[cIdx:]

      self.itemType = itemList[-1]
      self.itemList = itemList[:-1]

  #--------------------------------------------------------------------
  def DecomposeName(name):
    return NamedData.NamePath(name)

  def GetWsName(name):
    cIdx = 0
    for ch in name:
      if (ch == '.'):
        break
      cIdx += 1
    name = name[:cIdx]
    return name

  def StripWsName(name):
    cIdx = 0
    for ch in name:
      if (ch == '.'):
        break
      cIdx += 1
    name = name[cIdx+1:]
    return name

  #--------------------------------------------------------------------
  def CreateName(tblName,dataName):

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

    fullName = fullName + '.X.' + name

    #logging.debug('---------------------------------------------')
    #cnt = len(fullName)
    #logging.debug(str(cnt).rjust(3) + ' | ' + fullName)
    #logging.debug('---------------------------------------------')

    return fullName