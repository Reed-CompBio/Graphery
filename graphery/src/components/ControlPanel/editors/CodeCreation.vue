<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Code Editor
    </template>
    <template>
      <EditorFrame>
        <template v-slot:left>
          <q-card id="editor-wrapper" class="q-py-md q-px-sm q-mb-md">
            <div style="height: 70vh;" id="editor"></div>
            <q-inner-loading :showing="editor === null">
              <q-spinner-pie size="64px" color="primary" />
            </q-inner-loading>
          </q-card>

          <InfoCard>
            <template v-slot:title>
              <div class="q-mb-md">
                Exec JSON
              </div>
              <div class="q-mb-md">
                <q-select
                  :options="graphOptions"
                  v-model="graphChoice"
                  label="Select Graph"
                  outlined
                  clearable
                />
              </div>
              <div>
                <q-btn
                  label="Add Graph"
                  :loading="resultLoading"
                  class="q-mr-sm"
                />
                <q-btn label="Exec" :loading="resultLoading" class="q-mr-sm" />
                <q-btn
                  label="Exec Locally"
                  :loading="resultLoading"
                  class="q-mr-sm"
                />
                <q-btn
                  label="Exec All"
                  :loading="resultLoading"
                  class="q-mr-sm"
                />
                <q-btn
                  label="Exec All Locally"
                  :loading="resultLoading"
                  class="q-mr-sm"
                />
              </div>
            </template>
            <div>
              <q-input
                readonly
                class="half-height-textarea"
                v-model="resultJson"
                type="textarea"
                outlined
                label="Execution Result Json (Read Only)"
              />
              <q-inner-loading :showing="resultLoading">
                <q-spinner-pie size="48px" color="primary" />
              </q-inner-loading>
            </div>
          </InfoCard>
        </template>
        <template v-slot:right>
          <!-- TODO make this section follow the scrolling -->
          <div id="tutorial-selection">
            <InfoCard>
              <template v-slot:title>
                Tutorial
              </template>
              <q-select
                label="Tutorial"
                v-model="tutorialChoice"
                :options="tutorialOptions"
                outlined
                clearable
              ></q-select>
            </InfoCard>
          </div>

          <div id="submit-section">
            <!-- TODO button action -->
            <q-btn label="Submit" class="full-width"></q-btn>
            <!-- TODO align two sections -->
          </div>
        </template>
      </EditorFrame>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { mapState } from 'vuex';
  import loadingMixin from '../mixins/LoadingMixin';
  import pushToMixin from '../mixins/PushToMixin';

  export default {
    mixins: [loadingMixin, pushToMixin],
    components: {
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      EditorFrame: () => import('../frames/EditorFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        editor: null,
        tutorialChoice: '',
        tutorialOptions: [],
        graphChoice: '',
        graphOptions: [],
      };
    },
    computed: {
      ...mapState('settings', ['dark', 'fontSize']),
      resultJson() {
        return '';
      },
      resultLoading() {
        return false;
      },
    },
    methods: {
      isCreatingNew() {
        //
      },
    },
    mounted() {
      import('monaco-editor').then((md) => {
        this.editor = md.editor.create(document.getElementById('editor'), {
          fontSize: this.fontSize,
          foldingStrategy: 'indentation', // fold text by indentation
          automaticLayout: true, // auto resize
          overviewRulerBorder: false, // scroll bar no boarder
          scrollBeyondLastLine: false, // remove blank space at the end of the editor
          theme: this.dark ? 'vs-dark' : 'vs',
          language: 'python',
        });
      });
    },
  };
</script>
