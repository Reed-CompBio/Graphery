export default {
  /* TODO cy.style()
   *   .resetToDefault() // start a fresh default stylesheet
   *   .selector('node')
   *   .style('background-color', 'magenta')
   *   .update()
   * TODO add a strict version lol with <200b> unicode in it.
   */
  style: [
    {
      selector: 'node',
      css: {
        label: 'data(label)',
        'text-valign': 'bottom',
        'text-halign': 'center',
        height: '60px',
        width: '60px',
        'border-color': 'black',
        'border-opacity': '1',
        // 'background-image':
        //   'https://farm8.staticflickr.com/7272/7633179468_3e19e45a0c_b.jpg',
        'overlay-color': 'red',
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
          id: 'n0',
          label: 'N0',
          degree: '10',
        },
        scratch: {
          _degree: '20',
        },
        // node style
        style: {
          label: 'data(id)',
          // 'background-color': 'green',
          'overlay-color': 'lightblue',
        },
      },
      { data: { id: 'n1', label: 'N1' } },
      { data: { id: 'n2', label: 'N2' } },
      { data: { id: 'n3', label: 'N3' } },
      { data: { id: 'n4' } },
      { data: { id: 'n5' } },
      { data: { id: 'n6' } },
      { data: { id: 'n7' } },
      { data: { id: 'n8' } },
      { data: { id: 'n9' } },
      { data: { id: 'n10' } },
      { data: { id: 'n11' } },
      { data: { id: 'n12' } },
      { data: { id: 'n13' } },
      { data: { id: 'n14' } },
      { data: { id: 'n15' } },
      { data: { id: 'n16' } },
    ],
    edges: [
      { data: { source: 'n0', target: 'n1' } },
      { data: { source: 'n1', target: 'n2' } },
      { data: { source: 'n1', target: 'n3' } },
      { data: { source: 'n2', target: 'n7' } },
      { data: { source: 'n2', target: 'n11' } },
      { data: { source: 'n3', target: 'n4' } },
      { data: { source: 'n3', target: 'n16' } },
      { data: { source: 'n4', target: 'n5' } },
      { data: { source: 'n4', target: 'n6' } },
      { data: { source: 'n6', target: 'n8' } },
      { data: { source: 'n8', target: 'n9' } },
      { data: { source: 'n8', target: 'n10' } },
      { data: { source: 'n11', target: 'n12' } },
      { data: { source: 'n12', target: 'n13' } },
      { data: { source: 'n13', target: 'n14' } },
      { data: { source: 'n13', target: 'n15' } },
    ],
  },

  layout: {
    name: 'grid',
    padding: 5,
    fit: true,
  },
};
