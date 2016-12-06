import getopt
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

def createCompiledMultipleReplace(replacementsDict):
  regex = re.compile('|'.join(map(re.escape, replacementsDict)))
  return lambda text: regex.sub(lambda match: replacementsDict[match.group(0)], text)

removeCurlyBraces = createCompiledMultipleReplace({
  '{': '',
  '}': ''
})

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

def createCompositions(numRows, numColumns, includeZ = False):
  numTypes = 4
  if includeZ: numTypes += 1
  return compositions3(numTypes - 1, numRows * numColumns / 4)

def getBoardSizes(maxBoardSize):
  sizes = []
  for a in range(2, maxBoardSize + 1):
    for b in range(a, maxBoardSize + 1):
      if (a * b) % 4 is not 0: continue
      sizes.append([a, b])
  return sizes

DEFAULT_BOARD_SIZE = 4
MAX_BOARD_SIZE = 8

includeReflections = False
includeZType = False

def usage():
  print '''Usage:\n  -n <numRows> or --numrows <numRows>\t\tSpecifies the height of the board (Overridden by --boardsize)
  -m <numColumns> or --numcolumns <numColumns>\tSpecifies the width of the board (Overridden by --boardsize)
  -b <maxSize> or --boardsize <maxSize>\t\tSpecifies the maximum board size.
                                     \t\tWill run through all possible heights and widths up to
                                     \t\t<maxSize>x<maxSize> (Default 4)
  -r or --reflections\t\t\t\tInclude reflections (Default: False)
  -z or --ztype\t\t\t\t\tInclude Z-pieces (Default: False)
  -h or --help\t\t\t\t\tShows this help message\n'''
  sys.exit(2)

try:
  opts, _ = getopt.getopt(sys.argv[1:], 'hrzn:m:b:',['help', 'reflections', 'ztype', 'numrows=', 'numcolumns=', 'boardsize='])
except getopt.GetoptError as err:
  print err
  usage()

selectedN = False
selectedM = False
selectedBoardSize = False

boardSizes = []

def setNandM(n, m):
  if (n * m) % 4 is not 0:
    print 'Invalid numrows and numcolumns. Their product must be divisible by 4'
    sys.exit(2)
  boardSizes.append([n, m])

for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
  elif opt in ('-n', '--numrows'):
    if selectedBoardSize:
      print 'Cannot use -b and -n together. Overriding numrows with boardsize'
      continue
    try:
      n = int(arg)
      if n <= 0:
        print 'Number of rows must be positive, defaulting to {:d}'.format(DEFAULT_BOARD_SIZE)
        n = DEFAULT_BOARD_SIZE
      elif n > MAX_BOARD_SIZE:
        print 'Number of rows selected is too large, limiting to {:d}'.format(MAX_BOARD_SIZE)
        n = MAX_BOARD_SIZE
    except ValueError:
      print'Non numeric number of rows selected, defaulting to {:d}'.format(DEFAULT_BOARD_SIZE)
      n = DEFAULT_BOARD_SIZE
    if selectedM:
      setNandM(n, m)
    else:
      selectedN = True
  elif opt in ('-m', '--numcolumns'):
    if selectedBoardSize:
      print 'Cannot use -b and -m together. Overriding numcolumns with boardsize'
      continue
    try:
      m = int(arg)
      if m <= 0:
        print 'Number of columns must be positive, defaulting to {:d}'.format(DEFAULT_BOARD_SIZE)
        m = DEFAULT_BOARD_SIZE
      elif m > MAX_BOARD_SIZE:
        print 'Number of columns selected is too large, limiting to {:d}'.format(MAX_BOARD_SIZE)
        m = MAX_BOARD_SIZE
    except ValueError:
      print'Non numeric number of columns selected, defaulting to {:d}'.format(DEFAULT_BOARD_SIZE)
      m = DEFAULT_BOARD_SIZE
    if selectedN:
      setNandM(n, m)
    else:
      selectedM = True
  elif opt in ('-b', '--boardsize'):
    if (len(boardSizes) > 0):
      print 'Warning. Overriding chosen numrows and numcolumns with a range of board sizes'
    try:
      maxBoardSize = int(arg)
      if maxBoardSize < 2:
        print 'Board size must be at least 2, defaulting to {:d}'.format(DEFAULT_BOARD_SIZE)
        maxBoardSize = DEFAULT_BOARD_SIZE
      elif maxBoardSize > MAX_BOARD_SIZE:
        print 'Board size selected is too large, limiting to {:d}'.format(MAX_BOARD_SIZE)
        maxBoardSize = MAX_BOARD_SIZE
      elif maxBoardSize % 2 is not 0:
        print 'Board size must be even. Decrementing selected size by 1'
        maxBoardSize -= 1
    except ValueError:
      print'Non numeric board size selected, defaulting to {:d}'.format(DEFAULT_BOARD_SIZE)
      maxBoardSize = DEFAULT_BOARD_SIZE
    boardSizes = getBoardSizes(maxBoardSize)
    selectedBoardSize = True
  elif opt in ('-r', '--reflections'):
    includeReflections = True
  elif opt in ('-z', '--ztype'):
    includeZType = True
  else:
    usage()

if len(boardSizes) == 0:
  if selectedN:
    print 'Number of columns not selected. Using the same value as the given number of rows.'
    setNandM(n, n)
  elif selectedM:
    print 'Number of rows not selected. Using the same value as the given number of columns.'
    setNandM(m, m)
  else:
    print 'No board size selected. Defaulting to all boards up to {0:d}x{0:d}'.format(DEFAULT_BOARD_SIZE)
    boardSizes = getBoardSizes(DEFAULT_BOARD_SIZE)

if includeReflections:
  includedReflectionsString = 'Program run with reflections included'
else:
  includedReflectionsString =  'Program run with reflections not included'
print includedReflectionsString

if includeZType:
  includedZString = 'Program run with Z-pieces included'
  zCommentOpen = ''
  zCommentClose = ''
else:
  includedZString = 'Program run with Z-pieces not included'
  zCommentOpen = '/*'
  zCommentClose = '*/'
print includedZString

IDP_TEMPLATE_LOCATION = 'main.idp.template'
IDP_LOCATION = 'main.idp'

IDP_TEMPLATE_FILE = open('main.idp.template', 'r')
IDP_TEMPLATE = IDP_TEMPLATE_FILE.read()
IDP_TEMPLATE_FILE.close()

# Hard-code pieces of idp output to allow for easy extraction of data
UNSATISFIABLE_TEXT = 'Unsatisfiable\nNumber of models: 0\n'
SATISFIABLE_PRETEXT_LEN = len('Number of models: 1\nModel 1\n=======\nstructure  : Tetrominos {\n')
SATISFIABLE_POSTTEXT_LEN = len(' n = 4\n  nL = 0\n  nR = 0\n  nS = 4\n  nT = 0\n}\n\n')

def average(arr):
  if (len(arr) == 0): return 0
  s = 0
  for x in arr:
    s += x
  return float(s) / len(arr)

# Find all integer compositions for the given boardSize, format the IDP_TEMPLATE with the
# inputs and call idp, parsing and collecting the output, as well as the time taken, into JSON
def runIdp(numRows, numColumns):
  outputs = []
  totalTimer = getTimer()

  individualTimes = []
  numCompositions = 0

  didFinish = True

  for composition in createCompositions(numRows, numColumns, includeZType):
    nR = composition[0]
    nS = composition[1]
    nT = composition[2]
    nL = composition[3]
    if includeZType: nZ = composition[4]
    else: nZ = 0 
    try:
      numCompositions += 1

      if includeReflections:
        reflectionSpecification = ''
      else:
        reflectionSpecification = 'Reflected = {}'

      templated = multipleReplace(IDP_TEMPLATE, {
        '{nR}': str(nR),
        '{nS}': str(nS),
        '{nT}': str(nT),
        '{nL}': str(nL),
        '{nZ}': str(nZ),
        '{maxXIndex}': str(numColumns - 1),
        '{maxYIndex}': str(numRows - 1),
        '{numBlocks}': str(numRows * numColumns / 4),
        '{reflectionSpecification}': reflectionSpecification,
        '{zCommentOpen}': zCommentOpen,
        '{zCommentClose}': zCommentClose
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

        output = '{ blockLocations:'
        blockLocations = dict()
        hasLine = lines[1].split(' = ')[1]
        for has in hasLine.split(';'):
          hasPieces = has.split(',')
          x = int(hasPieces[0])
          y = int(hasPieces[1])
          blockId = int(hasPieces[2])
          if blockLocations.get(blockId) is None:
            blockLocations[blockId] = []
          blockLocations[blockId].append([x, y])

        output += '''{},
          nR: {:d},
          nS: {:d},
          nT: {:d},
          nL: {:d},
          nZ: {:d}
        }}'''.format(str(blockLocations), nR, nS, nT, nL, nZ)
        outputs.append(output)
    except KeyboardInterrupt:
      didFinish = False
      break

  return (
    outputs,
    totalTimer(),
    average(individualTimes),
    numCompositions,
    didFinish
  )

output = '['
for (iteration, boardSize) in enumerate(boardSizes):
  (numRows, numColumns) = boardSize

  print 'Iteration: {:d}\nBoard size: {:d}x{:d}'.format(iteration + 1, numRows, numColumns)

  (
    results,
    timeTaken,
    avgIdpCall,
    numCompositions,
    didFinish
  ) = runIdp(numRows, numColumns)

  output += '''
  {{
    numRows: {:d},
    numColumns: {:d},
    timeTaken: '{:.3f}s',
    results: ['''.format(numRows, numColumns, timeTaken) + ','.join(results) + '''],
    avgIdpCall: '{:.3f}s',
    numCompositions: {:d},
  }},'''.format(avgIdpCall, numCompositions)

  if not didFinish: break
output += ']'

HTML_OUTPUT_FILE = 'output.html'

incompleteWarning = ''
if not didFinish:
  incompleteWarning = 'Program was aborted before all compositions of the last iteration could complete'

# Pass the output into an html file via JSON so that the page can be generated in javascript
html = '''<html>
  <head>
    <link rel='stylesheet' href='styles.css'>
    <script>
      try {{
        eval(`var output = {};`);
      }} catch(e) {{
        console.error(e);
        var output = null;
      }}
    </script>
    <script src='project.js'></script>
  </head>
  <body>
    <div id="title">Tetromino Packing</div>
    <div id="subtitle">Jacob Patenaude - 301203788</div>
    <hr>
    <div id="runDetails">{}<br>{}</div>
    <hr>
    <div id="root">Loading...</div>
    <div id="incomplete">{}</div>
  </body>
</html>'''.format(output, includedReflectionsString, includedZString, incompleteWarning)


file = open(HTML_OUTPUT_FILE, 'w')
file.write(html)
file.close()

webbrowser.open_new_tab(HTML_OUTPUT_FILE)
