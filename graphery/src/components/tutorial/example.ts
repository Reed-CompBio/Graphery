export default {
  /* TODO cy.style(obj) and cy.removeStyle(name)
   * TODO add a strict version lol with <200b> unicode in it.
   */
  style: [
    {
      selector: 'node',
      css: {
        label: 'data(id)',
        'text-valign': 'bottom',
        'text-halign': 'center',
        height: '60px',
        width: '60px',
        'border-color': 'black',
        'border-opacity': '1',
        'background-image':
          'https://farm8.staticflickr.com/7272/7633179468_3e19e45a0c_b.jpg',
      },
    },
    {
      selector: 'edge',
      css: {
        'target-arrow-shape': 'triangle',
      },
    },
    {
      selector: ':selected',
      css: {
        'background-color': 'SteelBlue',
        'line-color': 'black',
        'target-arrow-color': 'black',
        'source-arrow-color': 'black',
      },
    },
    {
      selector: 'node.highlighted',
      style: {
        'border-width': '6px',
        'border-color': '#AAD8FF',
        'border-opacity': '0.5',
        'background-color': '#394855',
        'text-outline-color': '#394855',
      },
    },
  ],

  elements: {
    nodes: [
      {
        data: {
          id: 0,
          label: 'N0',
          degree: '10',
        },
        scratch: {
          _degree: '20',
        },
      },
      { data: { id: 1 } },
      { data: { id: 2 } },
      { data: { id: 3 } },
      { data: { id: 4 } },
      { data: { id: 5 } },
      { data: { id: 6 } },
      { data: { id: 7 } },
      { data: { id: 8 } },
      { data: { id: 9 } },
      { data: { id: 10 } },
      { data: { id: 11 } },
      { data: { id: 12 } },
      { data: { id: 13 } },
      { data: { id: 14 } },
      { data: { id: 15 } },
      { data: { id: 16 } },
    ],
    edges: [
      { data: { source: 0, target: 1 } },
      { data: { source: 1, target: 2 } },
      { data: { source: 1, target: 3 } },
      { data: { source: 2, target: 7 } },
      { data: { source: 2, target: 11 } },
      { data: { source: 3, target: 4 } },
      { data: { source: 3, target: 16 } },
      { data: { source: 4, target: 5 } },
      { data: { source: 4, target: 6 } },
      { data: { source: 6, target: 8 } },
      { data: { source: 8, target: 9 } },
      { data: { source: 8, target: 10 } },
      { data: { source: 11, target: 12 } },
      { data: { source: 12, target: 13 } },
      { data: { source: 13, target: 14 } },
      { data: { source: 13, target: 15 } },
    ],
  },

  layout: {
    name: 'grid',
    padding: 5,
    fit: true,
  },
};
