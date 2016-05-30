import sys
import os.path

#----------------------------------------------------------------------
def ParseArgs():
  args = {}

  pyPath,pyFile = os.path.split(sys.argv[0])

  if (len(sys.argv) != 2):
    print('usage: ' + pyFile + ' config-file')
    exit(-1)
  for i in range(1,len(sys.argv)):
    if (i == 1):
      args['CONFIG'] = sys.argv[1]

  return args