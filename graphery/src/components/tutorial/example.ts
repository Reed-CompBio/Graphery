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
          id: 'n0',
          label: 'N0',
          degree: '10',
        },
        scratch: {
          _degree: '20',
        },
      },
      {
        data: {
          id: 'n1',
          label: 'N1',
        },
      },
      {
        data: {
          id: 'n2',
          label: 'N2',
        },
      },
      {
        data: {
          id: 'n3',
          label: 'N3',
        },
      },
      {
        data: {
          id: 'n4',
        },
      },
      {
        data: {
          id: 'n5',
        },
      },
      {
        data: {
          id: 'n6',
        },
      },
      {
        data: {
          id: 'n7',
        },
      },
      {
        data: {
          id: 'n8',
        },
      },
      {
        data: {
          id: 'n9',
        },
      },
      {
        data: {
          id: 'n10',
        },
      },
      {
        data: {
          id: 'n11',
        },
      },
      {
        data: {
          id: 'n12',
        },
      },
      {
        data: {
          id: 'n13',
        },
      },
      {
        data: {
          id: 'n14',
        },
      },
      {
        data: {
          id: 'n15',
        },
      },
      {
        data: {
          id: 'n16',
        },
      },
    ],
    edges: [
      {
        data: {
          source: 'n0',
          target: 'n1',
          id: 0,
        },
      },
      {
        data: {
          source: 'n1',
          target: 'n2',
          id: 1,
        },
      },
      {
        data: {
          source: 'n1',
          target: 'n3',
          id: 2,
        },
      },
      {
        data: {
          source: 'n2',
          target: 'n7',
          id: 3,
        },
      },
      {
        data: {
          source: 'n2',
          target: 'n11',
          id: 4,
        },
      },
      {
        data: {
          source: 'n3',
          target: 'n4',
          id: 5,
        },
      },
      {
        data: {
          source: 'n3',
          target: 'n16',
          id: 6,
        },
      },
      {
        data: {
          source: 'n4',
          target: 'n5',
          id: 7,
        },
      },
      {
        data: {
          source: 'n4',
          target: 'n6',
          id: 8,
        },
      },
      {
        data: {
          source: 'n6',
          target: 'n8',
          id: 9,
        },
      },
      {
        data: {
          source: 'n8',
          target: 'n9',
          id: 10,
        },
      },
      {
        data: {
          source: 'n8',
          target: 'n10',
          id: 11,
        },
      },
      {
        data: {
          source: 'n11',
          target: 'n12',
          id: 12,
        },
      },
      {
        data: {
          source: 'n12',
          target: 'n13',
          id: 13,
        },
      },
      {
        data: {
          source: 'n13',
          target: 'n14',
          id: 14,
        },
      },
      {
        data: {
          source: 'n13',
          target: 'n15',
          id: 15,
        },
      },
    ],
  },
  layout: {
    name: 'grid',
    padding: 5,
    fit: true,
  },
};
