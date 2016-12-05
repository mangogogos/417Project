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

DEFAULT_NUM_ITER = 1
MAX_NUM_ITER = 5

includeReflections = False
numIter = DEFAULT_NUM_ITER

def usage(exit = True):
  print '''Usage:\n\t-n <numIter> or --iter <numIter>\tNumber of iterations
  \t-r or --reflections\t\t\tInclude reflections
  \t-h or --help\t\t\t\tShows this help message\n'''
  if exit: sys.exit(2)

try:
  opts, _ = getopt.getopt(sys.argv[1:], 'hrn:',['help', 'reflections', 'iter='])
except getopt.GetoptError as err:
  print err
  usage()

if len(opts) == 0:
  print 'No options specified. Running anyways with defaults.'
  usage(False)

selectedN = False
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
  elif opt in ('-n', '--iter'):
    selectedN = True
    try:
      numIter = int(arg)
      if (numIter > 0 and numIter <= MAX_NUM_ITER):
        print 'Running for {:d} iterations'.format(numIter)
      elif (numIter <= 0):
        print 'Number of iterations must be positive, defaulting to {:d}'.format(DEFAULT_NUM_ITER)
      else:
        print 'Number of iterations selected is too large, limiting to {:d}'.format(MAX_NUM_ITER)
        numIter = MAX_NUM_ITER
      if numIter > 1:
        print 'Warning. Iterations after the first one will likely take many hours to complete.'
    except ValueError:
      print'Non numeric number of iterations selected, defaulting to {:d}'.format(DEFAULT_NUM_ITER)
  elif opt in ('-r', '--reflections'):
    includeReflections = True
  else:
    usage()

if not selectedN:
  print 'Running for default number of iterations ({:d})'.format(DEFAULT_NUM_ITER)

if includeReflections:
  includedReflectionsString = 'Program run with reflections included'
else:
  includedReflectionsString =  'Program run with reflections not included'
print includedReflectionsString

IDP_TEMPLATE_LOCATION = 'main.idp.template'
IDP_LOCATION = 'main.idp'

IDP_TEMPLATE_FILE = open('main.idp.template', 'r')
IDP_TEMPLATE = IDP_TEMPLATE_FILE.read()
IDP_TEMPLATE_FILE.close()

# Hard-code pieces of idp output to allow for easy extraction of data
UNSATISFIABLE_TEXT = 'Unsatisfiable\nNumber of models: 0\n'
SATISFIABLE_PRETEXT_LEN = len('Number of models: 1\nModel 1\n=======\nstructure  : Tetriminos {\n')
SATISFIABLE_POSTTEXT_LEN = len(' n = 4\n  nL = 0\n  nR = 0\n  nS = 4\n  nT = 0\n}\n\n')

def average(arr):
  if (len(arr) == 0): return 0
  s = 0
  for x in arr:
    s += x
  return float(s) / len(arr)

# Find all integer compositions for the given boardSize, format the IDP_TEMPLATE with the
# inputs and call idp, parsing and collecting the output, as well as the time taken, into JSON
def runIdp(boardSize):
  outputs = []
  totalTimer = getTimer()

  individualTimes = []
  numCompositions = 0

  didFinish = True

  for (nR, nS, nT, nL) in createCompositions(boardSize):
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
        '{maxIndex}': str(boardSize - 1),
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
          nL: {:d}
        }}'''.format(str(blockLocations), nR, nS, nT, nL)
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

output = '{'
for iteration in range(numIter):
  boardSize = 4 + iteration * 2
  print 'Iteration: {0:d}\nBoard size: {1:d}x{1:d}'.format(iteration + 1, boardSize)

  (
    results,
    timeTaken,
    avgIdpCall,
    numCompositions,
    didFinish
  ) = runIdp(boardSize)

  output += '''{:d}:
  {{
    timeTaken: '{:.3f}s',
    results: ['''.format(boardSize, timeTaken) + ','.join(results) + '''],
    avgIdpCall: '{:.3f}s',
    numCompositions: {:d},
  }},'''.format(avgIdpCall, numCompositions)

  if not didFinish: break
output += '}'

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
    <div id="title">Tetrimino Packing</div>
    <div id="subtitle">Jacob Patenaude - 301203788</div>
    <hr>
    <div id="includedReflections">{}</div>
    <hr>
    <div id="root">Loading...</div>
    <div id="incomplete">{}</div>
  </body>
</html>'''.format(output, includedReflectionsString, incompleteWarning)


file = open(HTML_OUTPUT_FILE, 'w')
file.write(html)
file.close()

webbrowser.open_new_tab(HTML_OUTPUT_FILE)
