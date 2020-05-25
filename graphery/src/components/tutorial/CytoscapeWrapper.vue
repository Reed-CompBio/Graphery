<template>
  <div class="full-height ">
    <div id="cy-wrapper" class="full-height">
      <q-resize-observer @resize="resizeGraph" />
      <div id="cy" class="full-height" :style="graphStyle" ref="cy"></div>
    </div>
    <div>
      <q-inner-loading
        :showing="graphsEmpty || libLoading"
        transition-show="fade"
        transition-hide="fade"
      >
        <q-spinner-radio size="64px" color="primary" />
      </q-inner-loading>
    </div>
  </div>
</template>

<script>
  // import cytoscape from 'cytoscape';

  let cytoscape;
  let panzoom;
  let dagre;
  import { mapState, mapGetters, mapActions } from 'vuex';
  import {
    panzoomDefaults,
    dagreOptions,
    hierarchicalOptions,
  } from './config.js';

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
        selector: 0, // used in drop menu to select graphs
        moduleLoadedNum: 0,
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
      ...mapGetters('settings', ['graphBackgroundColor']),
      libLoading() {
        return this.moduleLoadedNum < 3;
      },
      currentGraph() {
        return this.getGraphByIndex(this.selector);
      },
      currentGraphId() {
        return this.currentGraph && this.currentGraph.id;
      },
      currentGraphJson() {
        return this.currentGraph && this.currentGraph.cyjs;
      },
      currentGraphLayoutEngine() {
        return this.currentGraph && this.currentGraph.layoutEngine;
      },
      graphStyle() {
        return {
          'background-color': this.graphBackgroundColor,
        };
      },
    },
    mounted() {
      import('cytoscape')
        .then((cy) => {
          // async load cytoscape
          cytoscape = cy.default;

          console.debug('cytoscape module: ', cy);

          // start init
          {
            const element = document.createElement('div');
            element.setAttribute('id', 'cy-mounting-point');
            element.setAttribute('class', 'cytoscape');
            element.setAttribute('class', 'full-height');

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
            console.debug('cy obj is mounted', this.cyInstance);

            // Force it to be painted again, so that when added to the DOM it doesn't show a blank graph
            this.$nextTick(() => {
              this.resizeGraph();
            });

            this.moduleLoad();
          }

          this.registerExtensions();
        })
        .catch((error) => {
          console.debug('error occur', error);
        });
    },
    methods: {
      moduleLoad() {
        this.moduleLoadedNum += 1;
      },
      ...mapActions('tutorials', ['clearAll']),
      /**
       * Triggers a graph resize, forcing it to repaint itself. Useful when the graph nodes and edges have been
       * modified, or when an older browser doesn't render the graph until it is resized.
       * @see https://github.com/cytoscape/cytoscape.js/issues/1748
       */
      registerExtensions() {
        import('cytoscape-panzoom').then((pz) => {
          console.debug('cytoscape panzoom module: ', pz);
          panzoom = pz.default;

          if (typeof cytoscape('core', 'panzoom') !== 'function') {
            panzoom(cytoscape);
          }

          this.cyInstance.panzoom(panzoomDefaults);

          this.$nextTick(() => {
            this.resizeGraph();
          });

          this.moduleLoad();
        });

        import('cytoscape-dagre').then((cd) => {
          console.debug('cytoscape dagre module: ', cd);
          dagre = cd.default;

          cytoscape.use(dagre);

          this.updateLayout();
          this.moduleLoad();
        });
      },
      /**
       * copied from
       * @see {@link https://github.com/cylc/cylc-ui/blob/master/src/components/cylc/graph/Graph.vue}
       */
      updateLayout() {
        switch (this.currentGraphLayoutEngine) {
          case 'dagre':
            this.layoutOptions = dagreOptions;
            this.runLayout(this.cyInstance, dagreOptions);
            break;
          case 'hac':
            this.cyInstance.elements().hca({
              mode: 'threshold',
              threshold: 25,
              distance: 'euclidean', // euclidean, squaredEuclidean, manhattan, max
              preference: 'mean', // median, mean, min, max,
              damping: 0.8, // [0.5 - 1]
              minIterations: 100, // [optional] The minimum number of iterations the algorithm will run before stopping (default 100).
              maxIterations: 1000, // [optional] The maximum number of iterations the algorithm will run before stopping (default 1000).
              attributes: [
                (node) => {
                  return node.data('weight');
                },
              ],
            });
            this.layoutOptions = hierarchicalOptions;
            this.runLayout(this.cyInstance, hierarchicalOptions);
            break;
          default:
            // Should never happen!
            this.layoutOptions = dagreOptions;
            this.runLayout(this.cyInstance, dagreOptions);
            break;
        }
      },
      /**
       * Runs the current layout.
       * @param {cytoscape} instance - the cytoscape instance
       * @param {*} [layoutOptions=null] - the layout options
       * @return {boolean} true if the layout ran successfully, false otherwise (e.g. manually stopped, temperature drop, etc)
       * @see {@link https://js.cytoscape.org/#cy.layout}
       * @see {@link https://github.com/cylc/cylc-ui/blob/master/src/components/cylc/graph/Graph.vue}
       */
      runLayout(instance, layoutOptions = null) {
        try {
          return instance
            .elements()
            .layout(layoutOptions || this.layoutOptions)
            .run();
        } catch (_) {
          // This is ignored, but can still be captured in the browser console, by checking the option to break on
          // exceptions, even if captured.
          //
          // The reason we need this, is that if the user has multiple components being displayed, and then closes one
          // of them while this code is running, it may cause an error saying that the layout is empty.
          // There is no action that we, or the user, can perform upon such error. Hence this being ignored.
        }
        return false;
      },
      resizeGraph() {
        if (this.cyInstance) {
          this.cyInstance.resize();
        }
      },
    },
    destroyed() {
      this.clearAll();
      // TODO restore states in vuex
    },
  };
</script>

<style>
  @import '~@/styles/panzoom.css';
</style>
