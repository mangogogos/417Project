// Generated from
// http://tools.medialab.sciences-po.fr/iwanthue/
const COLORS = [
  '#ff5a95',
  '#cb0062',
  '#de0048',
  '#952e3a',
  '#ff8c64',
  '#ffa988',
  '#c75900',
  '#ffb468',
  '#b17400',
  '#715000',
  '#f7bd40',
  '#a79300',
  '#d1ca4d',
  '#365d16',
  '#97d861',
  '#369400',
  '#0bab2d',
  '#89d986',
  '#006529',
  '#01d89c',
  '#01b4d8',
  '#ff0000',
  '#006398',
  '#028cdb',
  '#67b4ff',
  '#a2c2f8',
  '#0060d8',
  '#454b96',
  '#6f3b91',
  '#dea0ff',
  '#c44cd1',
  '#fa72f4',
  '#edb4e3',
  '#8e2a6d',
  '#ff58c4',
  '#d30091'
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

function generateRow({ blockLocations, nR, nS, nT, nL }, boardSize) {
  container = document.createElement('div');
  container.className = 'rowContainer';

  metaContainer = document.createElement('div');
  metaContainer.className = 'metaContainer';
  metaContainer.appendChild(document.createTextNode(`nR=${nR}`));
  metaContainer.appendChild(document.createElement('br'));
  metaContainer.appendChild(document.createTextNode(`nS=${nS}`));
  metaContainer.appendChild(document.createElement('br'));
  metaContainer.appendChild(document.createTextNode(`nT=${nT}`));
  metaContainer.appendChild(document.createElement('br'));
  metaContainer.appendChild(document.createTextNode(`nL=${nL}`));
  container.appendChild(metaContainer);

  const blockColors = generateColors(nR + nS + nT + nL);
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

  for (let x = 0; x < boardSize; x++) {
    const tilingRow = document.createElement('div');
    tilingRow.className = 'row';
    for (let y = 0; y < boardSize; y++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.style.backgroundColor = cellColors[x][y];
      cell.appendChild(document.createTextNode(cellBlockIds[x][y]));
      tilingRow.appendChild(cell);
    }
    tilingContainer.appendChild(tilingRow);
  }

  container.appendChild(tilingContainer);

  return container;
}

window.onload = function onLoad() {
  const rootElement = document.createElement('div');

  // otherwise output was not generated or passed correctly
  if (output) {
    Object.keys(output).forEach((boardSize, iterationNumber) =>
    {
      iterationNumber += 1; // index by 1 instead of by 0

      const {
        results,
        avgIdpCall,
        numCompositions,
        timeTaken,
      } = output[boardSize];

      numPackable = results.length;

      iterationRoot = document.createElement('div');
      iterationMetaContainer = document.createElement('div');
      iterationMetaContainer.className = 'iterationMeta';
      iterationMetaContainer.appendChild(document.createTextNode(`Iteration number: ${iterationNumber}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Board size: ${boardSize}x${boardSize}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Average IDP call: ${avgIdpCall}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Number packable: ${numPackable} out of ${numCompositions}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Total time taken: ${timeTaken}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationRoot.appendChild(iterationMetaContainer);

      for (composotion of results) {
        iterationRoot.appendChild(generateRow(composotion, boardSize));
      }

      rootElement.appendChild(iterationRoot);
      rootElement.appendChild(document.createElement('hr'));
    });
  } else {
    rootElement.appendChild(document.createTextNode('No valid output to show'));
  }

  const existingRoot = document.getElementById('root');
  existingRoot.replaceChild(rootElement, existingRoot.firstChild);
}
