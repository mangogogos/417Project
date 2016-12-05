// Shortened from
// http://godsnotwheregodsnot.blogspot.ca/2012/09/color-distribution-methodology.html
const COLORS = [
	'#FFFF00',
	'#1CE6FF',
	'#FF34FF',
	'#FF4A46',
	'#008941',
	'#006FA6',
	'#A30059',
  '#FFDBE5',
	'#7A4900',
	'#0000A6',
	'#63FFAC',
	'#B79762',
	'#004D43',
	'#8FB0FF',
	'#997D87',
  '#5A0007',
	'#809693',
	'#1B4400',
	'#4FC601',
	'#3B5DFF',
	'#4A3B53',
	'#FF2F80',
  '#61615A',
	'#BA0900',
	'#6B7900',
	'#00C2A0',
	'#FFAA92',
	'#FF90C9',
	'#B903AA',
	'#D16100',
	'#000035',
	'#7B4F4B',
	'#A1C299',
	'#300018',
	'#0AA6D8',
	'#013349',
	'#00846F',
  '#372101',
	'#FFB500',
	'#CC0744',
	'#C0B9B2',
	'#C2FF99',
	'#001E09',
  '#00489C',
	'#6F0062',
	'#0CBD66',
	'#EEC3FF',
	'#456D75',
	'#B77B68',
	'#7A87A1',
	'#788D66',
  '#885578',
	'#FAD09F',
	'#FF8A9A',
	'#D157A0',
	'#BEC459',
	'#456648',
	'#0086ED',
	'#886F4C',
  '#34362D',
	'#B4A8BD',
	'#00A6AA',
	'#452C2C',
	'#636375',
	'#FF913F',
	'#938A81',
  '#575329',
	'#00FECF',
	'#B05B6F',
	'#8CD0FF',
	'#3B9700',
	'#04F757',
	'#C8A1A1',
	'#1E6E00',
  '#7900D7',
	'#A77500',
	'#6367A9',
	'#A05837',
	'#6B002C',
	'#772600',
	'#D790FF',
	'#9B9700',
  '#549E79',
	'#201625',
	'#72418F',
	'#BC23FF',
	'#99ADC0',
	'#3A2465',
	'#922329',
  '#5B4534',
	'#404E55',
	'#0089A3',
	'#CB7E98',
	'#A4E804',
	'#324E72',
	'#6A3A4C',
];

function generateColors(nColors) {
  colors = {};
  existingColors = {};

  for (let i = 1; i <= nColors; i++) {
    let colorIndex;
    do {
      colorIndex = Math.floor(Math.random() * (COLORS.length + 1));
    } while (existingColors[colorIndex]);
    existingColors[colorIndex] = true;

    colors[i] = COLORS[colorIndex];
  }

  return colors;
}

function generateRow({ blockLocations, nR, nS, nT, nL }, n) {
  container = document.createElement('div');
  container.className = 'rowContainer';
  metaContainer = document.createElement('div');
  metaContainer.className = 'metaContainer';

  const metaText = document.createTextNode(`nR=${nR}, nS=${nS}, nT=${nT}, nL=${nL}`);
  metaContainer.appendChild(metaText);
  container.appendChild(metaContainer);

  const blockColors = generateColors(n);
  const cellColors = [];

  Object.keys(blockLocations).forEach(blockId =>
  {
    const color = blockColors[blockId];

    blockLocations[blockId].forEach(([x, y]) =>
    {
      cellColors[x] = cellColors[x] || [];
      cellColors[x][y] = color;
    });
  });

  const tilingContainer = document.createElement('div');
  tilingContainer.className = 'tilingContainer';

  for (let x = 0; x < n; x++) {
    const tilingRow = document.createElement('div');
    tilingRow.className = 'row';
    for (let y = 0; y < n; y++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      console.log(cellColors[x][y]);
      cell.style.backgroundColor = cellColors[x][y];
      tilingRow.appendChild(cell);
    }
    tilingContainer.appendChild(tilingRow);
  }

  container.appendChild(tilingContainer);

  return container;
}

window.onload = function onLoad() {
  const rootElement = document.createElement('div');
  Object.keys(output).forEach((boardSize, iterationNumber) =>
  {
    iterationNumber += 1; // index by 1 instead of by 0

    const {
      outputs,
      timeTaken,
    } = output[boardSize];
    iterationRoot = document.createElement('div');
    metaText = document.createTextNode( 'Iteration number: ' + iterationNumber +
                                      '. Board size: ' + boardSize + 'x' + boardSize +
                                      '. Time taken: ' + timeTaken);
    iterationRoot.appendChild(metaText);

    for (composotion of outputs) {
      iterationRoot.appendChild(generateRow(composotion, boardSize));
    }

    rootElement.appendChild(iterationRoot);
  });

  const existingRoot = document.getElementById('root');
  existingRoot.replaceChild(rootElement, existingRoot.firstChild);
}
