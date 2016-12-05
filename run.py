import re
import sys
import subprocess
import time
import webbrowser

def getTimer():
  start = time.time()
  return lambda: time.time() - start

# adapted from
# https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
def multipleReplace(text, replacementsDict):
  pattern = '|'.join(map(re.escape, replacementsDict))
  return re.sub(pattern, lambda match: replacementsDict[match.group(0)], text)

curlyBracesReplaceDict = {
  '{': '',
  '}': ''
}
def removeCurlyBraces(text):
  regex = re.compile('|'.join(map(re.escape, curlyBracesReplaceDict)))
  return regex.sub(lambda match: curlyBracesReplaceDict[match.group(0)], text)

# taken from
# https://gist.github.com/jasonmc/989158
def compositions3(t,s):
  for x in comp3(t,s,[0]*(t+1),0):
    yield x
    
def comp3(t,s,q,i=0):
  if i == t:
    q[i] = s
    yield q
  elif s == 0:
    yield q
  else:
    for x in range(s,-1,-1):
      u = q[:]
      u[i] = x
      for y in comp3(t,s-x,u,i+1):
        yield y            

def createCompositions(boardSize):
  return compositions3(3, boardSize * boardSize / 4)

INCLUDE_REFLECTIONS = True

# ------------------------------------------------------------------
# Read number of iterations to run from command line args

DEFAULT_NUM_ITER = 1
MAX_NUM_ITER = 5

IDP_TEMPLATE_LOCATION = 'main.idp.template'
IDP_LOCATION = 'main.idp'

numIter = DEFAULT_NUM_ITER
if len(sys.argv) > 1:
  try:
    numIter = int(sys.argv[1])
    if (numIter > 0 and numIter <= MAX_NUM_ITER):
      print('Running for ' + str(numIter) + ' iterations')
    elif (numIter <= 0):
      print('Number of iterations must be positive, defaulting to ' + str(DEFAULT_NUM_ITER))
    else:
      print('Number of iterations selected is too large, limiting to ' + str(MAX_NUM_ITER))
      numIter = MAX_NUM_ITER
  except ValueError:
    print('Non numeric number of iterations selected, defaulting to ' + str(DEFAULT_NUM_ITER))
else:
  print ('Running for default number of iterations (' + str(DEFAULT_NUM_ITER) + ')')

# ------------------------------------------------------------------

IDP_TEMPLATE_FILE = open('main.idp.template', 'r')
IDP_TEMPLATE = IDP_TEMPLATE_FILE.read()
IDP_TEMPLATE_FILE.close()

UNSATISFIABLE_TEXT = 'Unsatisfiable\nNumber of models: 0\n'
SATISFIABLE_PRETEXT_LEN = len('Number of models: 1\nModel 1\n=======\nstructure  : Tetriminos {\n')
SATISFIABLE_POSTTEXT_LEN = len(' n = 4\n  nL = 0\n  nR = 0\n  nS = 4\n  nT = 0\n}\n\n')

def average(arr):
  s = 0
  for x in arr:
    s += x
  return float(s) / len(arr)

def runIdp(boardSize):
  outputs = []
  totalTimer = getTimer()

  individualTimes = []
  numCompositions = 0

  for (nR, nS, nT, nL) in createCompositions(n):
    numCompositions += 1

    if INCLUDE_REFLECTIONS:
      reflectionSpecification = ''
    else:
      reflectionSpecification = 'Reflected = {}'

    templated = multipleReplace(IDP_TEMPLATE, {
      '{nR}': str(nR),
      '{nS}': str(nS),
      '{nT}': str(nT),
      '{nL}': str(nL),
      '{maxIndex}': str(boardSize-1),
      '{numBlocks}': str(boardSize * boardSize / 4),
      '{reflectionSpecification}': reflectionSpecification
    })

    IDP_FILE = open(IDP_LOCATION, 'w')
    IDP_FILE.write(templated)
    IDP_FILE.close()
    timer = getTimer()
    output = subprocess.check_output(['idp', IDP_LOCATION, '--nowarnings'])
    individualTimes.append(timer())
    if output != UNSATISFIABLE_TEXT:
      lines = removeCurlyBraces(
        output[SATISFIABLE_PRETEXT_LEN: -1 * SATISFIABLE_POSTTEXT_LEN]
      ).splitlines()
      # lines looks like:
      # BlockType = id, 'type'; ...
      # Has = x, y, id; ...
      # Located = id, x, y; ...
      # Reflected = id, reflected; ...
      # Rotated = id, 'rotation'; ...

      # output = '{ blockTypes: {'
      # blockTypeLine = lines[0].split(' = ')[1]
      # for blockType in blockTypeLine.split(';'):
      #   blockTypePieces = blockType.split(',')
      #   blockId = blockTypePieces[0].strip()
      #   blockType = blockTypePieces[1].strip()
      #   output += blockId + ':' + blockType + ','

      output = '{ blockLocations:'
      blockLocations = dict()
      hasLine = lines[1].split(' = ')[1]
      for has in hasLine.split(';'):
        hasPieces = has.split(',')
        x = hasPieces[0].strip()
        y = hasPieces[1].strip()
        blockId = hasPieces[2].strip()
        if blockLocations.get(blockId) is None:
          blockLocations[blockId] = []
        blockLocations[blockId].append([x, y])
      output += str(blockLocations) + ','
      output += 'nR: ' + str(nR) + ','
      output += 'nS: ' + str(nS) + ','
      output += 'nT: ' + str(nT) + ','
      output += 'nL: ' + str(nL) + '}'

      outputs.append(output)
  return (outputs, totalTimer(), average(individualTimes), numCompositions)

output = '{'
for iteration in range(numIter):
  n = 4 + iteration * 2
  print 'Iteration: ' + str(iteration + 1) + '\nBoard size: ' + str(n) + 'x' + str(n)
  try:
    (results, timeTaken, averageIdpCall, numCompositions) = runIdp(n)
  except KeyboardInterrupt:
    print "\nAborting. Only completed " + str(iteration) + " iterations out of " + str(numIter)
    break
  output += str(n) + ':{'
  output += 'timeTaken: ' + str(timeTaken) + ','
  output += 'results: [' + ','.join(results) + '],'
  output += 'avgIdpCall: ' + str(averageIdpCall) + ','
  output += 'numCompositions: ' + str(numCompositions) + '},'
output += '}'

if (iteration > 0):
  HTML_OUTPUT_FILE = 'output.html'

  html = '''<html>
    <head>
      <link rel='stylesheet' href='styles.css'>
      <script>var output = ''' + output + ''';</script>
      <script src='project.js'></script>
    </head>
    <body>
      <div id='root'>Loading...</div>
    </body>
  </html>'''

  file = open(HTML_OUTPUT_FILE, 'w')
  file.write(html)
  file.close()

  webbrowser.open_new_tab(HTML_OUTPUT_FILE)
