<template>
  <v-col cols="6">
    <!-- do not make v-rol the root element -->
    <v-skeleton-loader v-if="loading" type="image" class="fill-height">
    </v-skeleton-loader>
    <div id="cy" class="fill-height" ref="cy"></div>
  </v-col>
</template>

<script>
  import cytoscape from 'cytoscape';
  import { mapState, mapGetters } from 'vuex';

  const exampleContent = {
    style: [
      {
        selector: 'node',
        css: {
          content: 'data(id)',
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
          'background-color': 'black',
          'line-color': 'black',
          'target-arrow-color': 'black',
          'source-arrow-color': 'black',
        },
      },
    ],

    elements: {
      nodes: [
        { data: { id: 'n0' } },
        { data: { id: 'n1' } },
        { data: { id: 'n2' } },
        { data: { id: 'n3' } },
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
        { data: { source: 'n2', target: 'n16' } },
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

  export default {
    data() {
      return {
        cyInstance: null,
        // first loading wrapper, indicating the components like cytoscape are being loaded
        loading: true,
        selector: 0, // used in drop menu to select graphs
      };
    },
    computed: {
      ...mapState('settings', [
        'hideEdgeWhenRendering',
        'renderViewportOnly',
        'motionBlurEnabled',
        'motionSensitivityLevel',
      ]),
      ...mapGetters('tutorials', [
        'getGraphById',
        'getGraphByIndex',
        'articleEmpty',
        'graphsEmpty',
        'codesEmpty',
      ]),
      currentGraph() {
        return this.getGraphByIndex(this.selector);
      },
      currentGraphId() {
        return this.currentGraph ? this.currentGraph.id : null; // can't remember the syntax here
      },
      currentGraphJson() {
        return this.currentGraph ? this.currentGraph.cyjs : null;
      },
    },
    mounted() {
      const element = document.createElement('div');
      element.setAttribute('id', 'cytoscape');
      element.setAttribute('class', 'cytoscape');
      element.setAttribute('class', 'fill-height');
      this.$refs.cy.appendChild(element);
      // When passing objects to Cytoscape.js for creating elements, animations, layouts, etc.,
      // the objects are considered owned by Cytoscape. __** this may cause conflicts when workint with vuex **__
      // When desired, the programmer can copy objects manually before passing them to Cytoscape. However,
      // copying is not necessary for most programmers most of the time.
      //
      // cannot use get element by id
      // NOTE: Vue will try to create observers for each property in this nested cytoscape object
      //       and it crashed my browser several times. By freezing it, we tell Vue to not bother
      //       about it. This isn't a reactive property anyway, just a variable in the component.
      this.cyInstance = Object.freeze(
        cytoscape({
          container: element,
          // animation settings
          textureOnViewport: this.renderViewportOnly,
          hideEdgesOnViewport: this.hideEdgeWhenRendering,
          motionBlur: this.motionBlurEnabled,

          zoom: 1,
          styleEnabled: true,
          ...exampleContent,
        })
      );

      console.log('cy obj is mounted', this.cyInstance);

      // Force it to be painted again, so that when added to the DOM it doesn't show a blank graph
      this.$nextTick(() => {
        this.resizeGraph();
      });

      this.loading = false;
    },
    methods: {
      /**
       * Triggers a graph resize, forcing it to repaint itself. Useful when the graph nodes and edges have been
       * modified, or when an older browser doesn't render the graph until it is resized.
       * @see https://github.com/cytoscape/cytoscape.js/issues/1748
       */
      resizeGraph() {
        this.cyInstance.resize();
      },
    },
    destroyed() {
      // TODO restore states in vuex
    },
  };
</script>

<style>
  #cy {
    background-color: #fff;
  }
</style>
