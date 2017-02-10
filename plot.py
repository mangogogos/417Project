import matplotlib.pyplot as plt
from collections import Counter

SIZES = [
  '2x2',
  '2x4',
  '3x4',
  '4x4'
]
sizePositions = range(1, len(SIZES) + 1)

CATEGORIES = [
  'No reflections or Z-pieces',
  'Only reflections',
  'Only Z-pieces',
  'Both reflections and Z-pieces',
]

times = {
  CATEGORIES[0]: {
    'Average IDP call': ['0.179', '0.191', '0.179', '0.297'],
    'Total time taken': ['0.716', '1.912', '3.582', '10.390'],
  },
  CATEGORIES[1]: {
    'Average IDP call': ['0.192', '0.197', '0.234', '0.381'],
    'Total time taken': ['0.768', '1.974', '4.686', '13.351'],
  },
  CATEGORIES[2]: {
    'Average IDP call': ['0.243', '0.243', '0.243', '0.363'],
    'Total time taken': ['1.216', '3.651', '8.521', '25.398'],
  },
  CATEGORIES[3]: {
    'Average IDP call': ['0.246', '0.243', '0.243', '0.444'],
    'Total time taken': ['1.232', '3.644', '8.503', '31.075'],
  }
}

AVERAGE_FIGURE = 1
TOTAL_FIGURE = 2

for category in CATEGORIES:
  plt.figure(AVERAGE_FIGURE)
  plt.plot(sizePositions, times[category]['Average IDP call'], label = category)

  plt.figure(TOTAL_FIGURE)
  plt.plot(sizePositions, times[category]['Total time taken'], label = category)

plt.figure(AVERAGE_FIGURE)
plt.xticks(sizePositions, SIZES)
plt.legend(loc='best')
plt.title('Average IDP Call for each Board Size')
plt.ylabel('Average IDP Call (seconds)')
plt.xlabel('Board Size')
plt.savefig('average.png')

plt.figure(TOTAL_FIGURE)
plt.xticks(sizePositions, SIZES)
plt.legend(loc='best')
plt.title('Total runtime for each Board Size')
plt.ylabel('Time (seconds)')
plt.xlabel('Board Size')
plt.savefig('total.png')