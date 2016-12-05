// Generated from
// http://tools.medialab.sciences-po.fr/iwanthue/
const COLORS = [
  '#2499d7',
  '#bab237',
  '#4f54b7',
  '#9cb24e',
  '#8e78e5',
  '#56a555',
  '#bf68c4',
  '#45c097',
  '#553382',
  '#cb8130',
  '#5486e5',
  '#8d8137',
  '#9283ce',
  '#a93f2a',
  '#cd68af',
  '#d17b54',
  '#882860',
  '#df6574',
  '#9b2c41',
  '#d76092'
];

function generateColors(nColors) {
  colors = {};
  existingColors = {};

  for (let i = 1; i <= nColors; i++) {
    let colorIndex;
    do {
      colorIndex = Math.floor(Math.random() * COLORS.length);
    } while (existingColors[colorIndex]);
    existingColors[colorIndex] = true;

    if (!COLORS[colorIndex]) {
      console.log(colorIndex);
    }

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

  const blockColors = generateColors(n * n / 4);
  const cellColors = [];
  const cellBlockIds = [];

  Object.keys(blockLocations).forEach(blockId =>
  {
    const color = blockColors[blockId];

    blockLocations[blockId].forEach(([x, y]) =>
    {
      cellColors[x] = cellColors[x] || [];
      cellColors[x][y] = color;

      cellBlockIds[x] = cellBlockIds[x] || [];
      cellBlockIds[x][y] = blockId;
    });
  });

  const tilingContainer = document.createElement('div');
  tilingContainer.className = 'tilingContainer';

  for (let x = 0; x < n; x++) {
    const tilingRow = document.createElement('div');
    tilingRow.className = 'row';
    for (let y = 0; y < n; y++) {
      const cell = document.createElement('div');
      const cellBlockId = document.createTextNode(cellBlockIds[x][y]);
      cell.className = 'cell';
      cell.style.backgroundColor = cellColors[x][y];
      cell.appendChild(cellBlockId);
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
      results,
      avgIdpCall,
      numCompositions,
      timeTaken,
    } = output[boardSize];
    iterationRoot = document.createElement('div');
    metaText = document.createTextNode( 'Iteration number: ' + iterationNumber +
                                      '. Board size: ' + boardSize + 'x' + boardSize +
                                      '. Average IDP call: ' + avgIdpCall +
                                      '. Number of Compositions: ' + numCompositions +
                                      '. Total time taken: ' + timeTaken);
    iterationRoot.appendChild(metaText);

    for (composotion of results) {
      iterationRoot.appendChild(generateRow(composotion, boardSize));
    }

    rootElement.appendChild(iterationRoot);
  });

  const existingRoot = document.getElementById('root');
  existingRoot.replaceChild(rootElement, existingRoot.firstChild);
}
