<template>
  <div style="overflow: hidden; ">
    <q-splitter
      v-if="$q.screen.gt.xs"
      v-model="splitPos"
      :style="splitterStyle"
      :horizontal="verticalSplitter"
      :separator-class="
        verticalSplitter
          ? 'resizable-h-separator-splitter'
          : 'resizable-v-separator-splitter'
      "
    >
      <template v-slot:before>
        <CytoscapeWrapper ref="cytoscapeWrapper"></CytoscapeWrapper>
      </template>
      <template v-slot:separator>
        <SplitterSeparator :horizontal="verticalSplitter" />
      </template>
      <template v-slot:after>
        <div>
          <q-bar class="graph-menu-bar">
            <div class="graph-menu-wrapper">
              <q-select
                class="graph-selector"
                :options="codeOptions"
                v-model="codeChoice"
                label="Code"
                :multiple="false"
                dropdown-icon="mdi-menu-down"
                :loading="codeListEmpty"
                emit-value
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      No results
                    </q-item-section>
                  </q-item>
                </template>
                <template v-slot:prepend>
                  <q-icon name="code"></q-icon>
                </template>
              </q-select>
            </div>
          </q-bar>
          <EditorWrapper
            style="max-height: calc(100% - 56px);"
            @updateCyWithVarObj="updateCytoscapeWithVarObj"
          ></EditorWrapper>
        </div>
      </template>
    </q-splitter>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import { headerSize } from '@/store/states/meta';
  import { apiCaller } from '@/services/apis';
  import { pullGraphAndCodeQuery } from '@/services/queries';
  import { errorDialog, warningDialog } from '@/services/helpers';
  import SplitterSeparator from '../components/framework/SplitterSeparator';
  import { emptyCodeTemplate, newModelUUID } from '@/services/params';

  const defaultCodeOption = [
    {
      label: 'Default Empty Template',
      value: newModelUUID,
    },
  ];

  const defaultCodeSnippet = (() => {
    const obj = {};
    obj[newModelUUID] = emptyCodeTemplate;
    return obj;
  })();

  export default {
    props: ['url'],
    components: {
      SplitterSeparator,
      EditorWrapper: () => import('@/components/tutorial/EditorWrapper.vue'),
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
    },
    data() {
      return {
        codeChoice: null,
        codeOptions: defaultCodeOption,
        codeSnippets: defaultCodeSnippet,
      };
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
      splitPos: {
        set(d) {
          this.$store.dispatch(
            'settings/changeGraphSplitPos',
            Math.round(d * 10) / 10
          );
        },
        get() {
          return this.graphSplitPos;
        },
      },
      splitterStyle() {
        return {
          height: `calc(100vh - ${headerSize}px)`,
        };
      },
      codeListEmpty() {
        return this.codeOptions === null || this.codeOptions.length === 0;
      },
      requestPayload() {
        return {
          url: this.url,
        };
      },
      currentCode() {
        if (!this.codeListEmpty && this.codeSnippets) {
          return this.codeSnippets[this.codeChoice];
        }
        return null;
      },
      verticalSplitter() {
        return this.$q.screen.lt.md;
      },
    },
    methods: {
      generateDefaultJsonResults(graphId) {
        return [
          {
            json: '[]',
            graphId,
            codeId: newModelUUID,
          },
        ];
      },
      loadGraphAndCode() {
        apiCaller(pullGraphAndCodeQuery, this.requestPayload)
          .then((data) => {
            if (!data || !('graph' in data)) {
              throw Error('Invalid data returned');
            }

            const graphObj = data.graph;

            this.$store.dispatch('tutorials/loadTutorialGraphs', [
              {
                id: graphObj.id,
                cyjs: graphObj.cyjs,
                isPublished: graphObj.isPublished,
                content: graphObj.content,
                priority: graphObj.priority,
              },
            ]);

            this.codeOptions = defaultCodeOption;
            const resultJsonList = this.generateDefaultJsonResults(graphObj.id);
            this.codeSnippets = defaultCodeSnippet;

            if (graphObj.execresultjsonSet.length > 0) {
              graphObj.execresultjsonSet.forEach((obj) => {
                this.codeOptions.push({
                  label: obj.code.id,
                  value: obj.code.id,
                });

                resultJsonList.push({
                  json: obj.json,
                  graphId: graphObj.id,
                  codeId: obj.code.id,
                });

                this.codeSnippets[obj.code.id] = obj.code.code;
              });
            } else {
              warningDialog({
                message: 'This graph has no code associated with it!',
              });
            }

            if (this.codeOptions.length > 0) {
              this.codeChoice = this.codeOptions[0].value;
            }

            this.$store.dispatch(
              'tutorials/loadTutorialResultJsonList',
              resultJsonList
            );
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching graph and code. ${err}`,
            });
          });
      },
      updateCytoscapeWithVarObj(varObj) {
        this.$refs.cytoscapeWrapper.highlightVarObj(varObj);
      },
    },
    mounted() {
      this.loadGraphAndCode();
    },
    watch: {
      codeChoice: function() {
        this.$store.commit('tutorials/LOAD_CURRENT_CODE_ID', this.codeChoice);
        this.$store.commit('tutorials/LOAD_CODES', this.currentCode);
      },
    },
    destroyed() {
      this.$store.dispatch('tutorials/clearAll');
    },
  };
</script>
