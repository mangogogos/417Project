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
  '#5e5766',
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

function generateComposition({ blockLocations, nR, nS, nT, nL, nZ }, numRows, numColumns) {
  composotionContainer = document.createElement('div');
  composotionContainer.className = 'composotionContainer';

  composotionMetaContainer = document.createElement('div');
  composotionMetaContainer.className = 'composotionMetaContainer';
  composotionMetaContainer.appendChild(document.createTextNode(`nR=${nR}`));
  composotionMetaContainer.appendChild(document.createElement('br'));
  composotionMetaContainer.appendChild(document.createTextNode(`nS=${nS}`));
  composotionMetaContainer.appendChild(document.createElement('br'));
  composotionMetaContainer.appendChild(document.createTextNode(`nT=${nT}`));
  composotionMetaContainer.appendChild(document.createElement('br'));
  composotionMetaContainer.appendChild(document.createTextNode(`nL=${nL}`));
  composotionMetaContainer.appendChild(document.createElement('br'));
  composotionMetaContainer.appendChild(document.createTextNode(`nZ=${nZ}`));
  composotionContainer.appendChild(composotionMetaContainer);

  const blockColors = generateColors(nR + nS + nT + nL + nZ);

  const cellColors = [];
  const cellBlockIds = [];

  Object.keys(blockLocations).forEach(blockId =>
  {
    const color = blockColors[blockId];

    // Technically this is supposed to be x, y but I'm redefining the origin to be the top left as opposed to the top right for easier html rendering
    // I suppose I couuuulld go back and rewrite my idp specification to use a top-left origin but why would I want to do that when this is easier?
    blockLocations[blockId].forEach(([y, x]) =>
    {
      cellColors[x] = cellColors[x] || [];
      cellColors[x][y] = color;

      cellBlockIds[x] = cellBlockIds[x] || [];
      cellBlockIds[x][y] = blockId;
    });
  });

  const compositionTilingContainer = document.createElement('div');
  compositionTilingContainer.className = 'compositionTilingContainer';

  for (let y = 0; y < numColumns; y++) {
    const tilingColumn = document.createElement('div');
    tilingColumn.className = 'column';
    for (let x = 0; x < numRows; x++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.style.backgroundColor = cellColors[x][y];
      cell.appendChild(document.createTextNode(cellBlockIds[x][y]));
      tilingColumn.appendChild(cell);
    }
    compositionTilingContainer.appendChild(tilingColumn);
  }

  composotionContainer.appendChild(compositionTilingContainer);

  return composotionContainer;
}

window.onload = function onLoad() {
  const rootElement = document.createElement('div');

  // otherwise output was not generated or passed correctly
  if (output) {
    output.forEach(({ results, avgIdpCall, numCompositions, timeTaken, numRows, numColumns }, iterationNumber) =>
    {
      iterationNumber += 1; // index by 1 instead of by 0

      numPackable = results.length;

      iterationRoot = document.createElement('div');
      iterationMetaContainer = document.createElement('div');
      iterationMetaContainer.className = 'iterationMeta';
      iterationMetaContainer.appendChild(document.createTextNode(`Iteration number: ${iterationNumber}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Board size: ${numRows}x${numColumns}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Average IDP call: ${avgIdpCall}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Number packable: ${numPackable} out of ${numCompositions}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationMetaContainer.appendChild(document.createTextNode(`Total time taken: ${timeTaken}`));
      iterationMetaContainer.appendChild(document.createElement('br'));
      iterationRoot.appendChild(iterationMetaContainer);

      for (composotion of results) {
        iterationRoot.appendChild(generateComposition(composotion, numRows, numColumns));
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
