<template>
  <div class="full-height">
    <q-bar class="graph-menu-bar">
      <div class="graph-menu-wrapper">
        <q-select
          class="graph-selector"
          :options="getGraphList"
          v-model="graphChoice"
          label="Graph"
          :multiple="false"
          dropdown-icon="mdi-menu-down"
          :loading="graphsEmpty"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">
                No results
              </q-item-section>
            </q-item>
          </template>
          <template v-slot:prepend>
            <q-icon name="mdi-graphql"></q-icon>
          </template>
        </q-select>
      </div>
      <div class="menu-button-group-wrapper">
        <q-btn-group rounded class="menu-button-group q-mx-auto">
          <q-btn>
            <q-icon name="mdi-file-table-box" />
            <SwitchTooltip :text="$t('tooltips.graphInfo')"></SwitchTooltip>
          </q-btn>
          <q-btn-dropdown>
            <template v-slot:label>
              <q-icon name="mdi-share-variant" />
              <SwitchTooltip :text="$t('tooltips.Share')"></SwitchTooltip>
            </template>
          </q-btn-dropdown>
        </q-btn-group>
      </div>
    </q-bar>
    <div id="cy-wrapper" :style="heightStyle">
      <div id="cy" class="full-height" :style="graphStyle" ref="cy"></div>
    </div>
    <div>
      <q-inner-loading
        :showing="graphsEmpty || libLoading"
        transition-show="fade"
        transition-hide="fade"
      >
        <q-spinner-pie size="64px" color="primary" />
      </q-inner-loading>
    </div>
  </div>
</template>

<script>
  let cytoscape;
  let panzoom;
  let dagre;
  let Tippy;
  let popper;

  import { graphMenuHeaderSize } from '../../store/states/meta';
  import { mapState, mapGetters } from 'vuex';
  import {
    panzoomDefaults,
    dagreOptions,
    hierarchicalOptions,
  } from './config.js';

  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
    },
    data() {
      return {
        cyInstance: null,
        moduleLoadedNum: 0,
        moduleTargetNum: 5,
        tippy: null,
        testValue: 0,
        lastVarObj: {},
        choseGraphObj: null,
        currentGraphLayoutEngine: 'dagre',
        // TODO remember to clear this out
      };
    },
    computed: {
      ...mapState('settings', [
        'hideEdgeWhenRendering',
        'renderViewportOnly',
        'motionBlurEnabled',
        'motionSensitivityLevel',
      ]),
      // TODO watch to every cy options
      ...mapState('tutorials', ['currentGraphId']),
      ...mapGetters('tutorials', [
        'getGraphList',
        'getGraphById',
        'getGraphByIndex',
        'graphsEmpty',
        'currentGraph',
        'currentGraphJsonObj',
      ]),
      ...mapGetters('settings', ['graphBackgroundColor']),
      graphChoice: {
        get() {
          return this.choseGraphObj;
        },
        set(choseGraphObj) {
          if (choseGraphObj && choseGraphObj !== this.choseGraphObj) {
            this.choseGraphObj = choseGraphObj;
            this.$store.commit(
              'tutorials/LOAD_CURRENT_GRAPH_ID',
              choseGraphObj.value
            );
          }
        },
      },
      libLoading() {
        return this.moduleLoadedNum < this.moduleTargetNum;
      },
      graphStyle() {
        return {
          'background-color': this.graphBackgroundColor,
        };
      },
      heightStyle() {
        return {
          height: `calc(100% - ${graphMenuHeaderSize}px)`,
        };
      },
    },
    methods: {
      moduleLoad() {
        this.moduleLoadedNum += 1;
      },
      registerExtensions() {
        import('cytoscape-panzoom').then((pz) => {
          console.debug('cytoscape panzoom module: ', pz);
          panzoom = pz.default;

          if (typeof cytoscape('core', 'panzoom') !== 'function') {
            cytoscape.use(panzoom);
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

        import('cytoscape-popper')
          .then((pp) => {
            console.debug('cytoscape popper module: ', pp);

            popper = pp.default;
            if (typeof cytoscape('core', 'popper') !== 'function') {
              cytoscape.use(popper);
            }
            this.moduleLoad();
          })
          .then(() => {
            import('tippy.js')
              .then((tp) => {
                console.debug('Tippy module: ', tp);
                Tippy = tp.default;
                this.moduleLoad();
              })
              .then(() => {
                this.setupTooltips(this.cyInstance);
              });
          });
      },
      makeTippy(node, text) {
        const ref = node.popperRef();
        const dummyDomEle = document.createElement('div');
        return Tippy(dummyDomEle, {
          onCreate: function(instance) {
            instance.popperInstance.reference = ref;
          },
          lazy: false, // mandatory
          trigger: 'manual', // mandatory

          // dom element inside the tippy:
          content: function() {
            // function can be better for performance
            const div = document.createElement('div');

            div.innerHTML = text;

            return div;
          },

          // your own preferences:
          arrow: true,
          placement: 'bottom',
          theme: 'material',
          hideOnClick: 'true',
          delay: [0, 2000],
          animation: 'fade',
          multiple: false,
          flip: true,
          flipOnUpdate: true,
          duration: [250, 275],
          allowHTML: true,
          touch: true,
          // sticky: 'popper', // don't need it

          // if interactive:
          interactive: true,
          appendTo: document.body, // or append dummyDomEle to document.body
        });
      },
      closeTippy() {
        if (this.tippy !== null) {
          this.tippy.hide();
        }
      },
      setupTooltips(instance) {
        // show node tooltips
        instance.on('mouseover', 'node', (event) => {
          const node = event.target;
          this.tippy = this.makeTippy(node, `test content ${this.testValue}`);
          this.tippy.show();
        });
        instance.on('mouseout', 'node', (_) => {
          this.closeTippy();
        });

        // show edge tooltips
        instance.on('mouseover', 'edge', (event) => {
          const node = event.target;
          this.tippy = this.makeTippy(node, `test content ${this.testValue}`);
          this.tippy.show();
        });

        instance.on('mouseout', 'edge', (_) => {
          this.closeTippy();
        });
      },
      reloadCyWithFullJson(json) {
        if (this.cyInstance && json) {
          this.cyInstance.elements().remove();
          this.cyInstance.add(json.elements);
          if (json.style) {
            this.cyInstance
              .style()
              .resetToDefault()
              .fromJson(json.style)
              .update();
          }
        }
      },
      // highlight helper function
      highlightElement(id, color) {
        this.cyInstance.getElementById(id).style({
          'overlay-color': color,
          'overlay-opacity': 0.5,
        });
      },
      unhighlightElement(id) {
        this.cyInstance.getElementById(id).removeStyle('overlay-opacity');
      },
      // highlight interface
      highlightVarObj(varObj) {
        if (varObj) {
          for (const [varName, varValue] of Object.entries(varObj)) {
            if (varValue && typeof varValue === 'object') {
              if (this.lastVarObj[varName] !== varValue['id']) {
                this.unhighlightElement(this.lastVarObj[varName]);
                this.lastVarObj[varName] = varValue['id'];
              }

              this.highlightElement(varValue['id'], varValue['color']);
            }
          }
        }
      },
      reloadGraph() {
        this.cyInstance.style().resetToDefault();
        this.reloadCyWithFullJson(this.currentGraphJsonObj);
        this.updateLayout();
      },
      updateLayout() {
        /**
         * copied from
         * @see {@link https://github.com/cylc/cylc-ui/blob/master/src/components/cylc/graph/Graph.vue}
         */
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
      runLayout(instance, layoutOptions = null) {
        /**
         * Runs the current layout.
         * @param {cytoscape} instance - the cytoscape instance
         * @param {*} [layoutOptions=null] - the layout options
         * @return {boolean} true if the layout ran successfully, false otherwise (e.g. manually stopped, temperature drop, etc)
         * @see {@link https://js.cytoscape.org/#cy.layout}
         * @see {@link https://github.com/cylc/cylc-ui/blob/master/src/components/cylc/graph/Graph.vue}
         */
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
      /**
       * Triggers a graph resize, forcing it to repaint itself. Useful when the graph nodes and edges have been
       * modified, or when an older browser doesn't render the graph until it is resized.
       * @see https://github.com/cytoscape/cytoscape.js/issues/1748
       */
      resizeGraph() {
        if (this.cyInstance) {
          this.cyInstance.resize();
        }
      },
    },
    watch: {
      getGraphList: function() {
        this.graphChoice = this.getGraphList[0];
      },
      currentGraph: function() {
        this.reloadGraph();
      },
    },
    mounted() {
      import('cytoscape')
        .then((cy) => {
          // async load cytoscape
          cytoscape = cy.default;

          console.debug('cytoscape module: ', cy);
        })
        .then(() => {
          // start init

          const element = document.createElement('div');
          element.setAttribute('id', 'cy-mounting-point');
          element.setAttribute('class', 'cytoscape');
          element.setAttribute('class', 'full-height');

          this.$refs.cy.appendChild(element);

          /*
           * When passing objects to Cytoscape.js for creating elements, animations, layouts, etc.,
           * the objects are considered owned by Cytoscape. __** this may cause conflicts when working with vuex **__
           * When desired, the programmer can copy objects manually before passing them to Cytoscape. However,
           * copying is not necessary for most programmers most of the time.
           *
           * cannot use get element by id
           * NOTE: Vue will try to create observers for each property in this nested cytoscape object
           *       and it crashed my browser several times. By freezing it, we tell Vue to not bother
           *       about it. This isn't a reactive property anyway, just a variable in the component.
           *
           */

          this.cyInstance = Object.freeze(
            cytoscape({
              container: element,
              // animation settings
              textureOnViewport: this.renderViewportOnly,
              hideEdgesOnViewport: this.hideEdgeWhenRendering,
              motionBlur: this.motionBlurEnabled,
              zoom: 1,
              styleEnabled: true,
            })
          );
          console.debug('cy obj is mounted', this.cyInstance);

          this.graphChoice = this.getGraphList[0];
          this.reloadGraph();

          // Force it to be painted again, so that when added to the DOM it doesn't show a blank graph
          this.$nextTick(() => {
            this.resizeGraph();
          });

          this.moduleLoad();
        })
        .then(() => {
          this.registerExtensions();
        })
        .catch((error) => {
          // TODO load up popup
          console.error('error occur', error);
        });
    },
    beforeDestroy() {
      this.closeTippy();
    },
  };
</script>

<style lang="sass">
  @import '~@/styles/panzoom.css'
  @import '~tippy.js/dist/tippy.css'

  .graph-menu-bar
    min-height: 56px
    max-height: 56px
    display: flex
    flex-direction: row
    .graph-menu-wrapper
      padding: 0 5px
      margin: 0 15px
      min-width: 50%
      max-height: inherit

    .menu-button-group-wrapper
      margin: auto 5px
</style>
