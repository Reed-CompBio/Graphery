<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Code Editor
    </template>
    <template>
      <EditorFrame>
        <template v-slot:left>
          <IDCard :id="codeObject.id" />
          <q-card id="editor-wrapper" class="q-py-md q-px-sm q-mb-md">
            <div style="height: 70vh;" id="editor"></div>
            <q-inner-loading :showing="editor === null">
              <q-spinner-pie size="64px" color="primary" />
            </q-inner-loading>
          </q-card>
        </template>
        <template v-slot:right>
          <!-- TODO make this section follow the scrolling -->
          <div id="tutorial-selection">
            <TutorialSelection v-model="codeObject.tutorial" single-selection />
          </div>

          <div id="submit-section">
            <!-- TODO button action -->
            <SubmitButton class="full-width" :action="postCode" />
          </div>
        </template>
      </EditorFrame>
      <EditorFrame>
        <template v-slot:left>
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
          <SubmitButton class="full-width" :action="postExecJson" />
        </template>
      </EditorFrame>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { mapState } from 'vuex';
  import loadingMixin from '../mixins/LoadingMixin';
  import pushToMixin from '../mixins/PushToMixin';
  import SubmitButton from '../parts/SubmitButton';
  import IDCard from '../parts/IDCard';
  import { newModelUUID } from '../../../services/params';
  import { apiCaller } from '../../../services/apis';
  import { codeQuery, updateCodeMutation } from '../../../services/queries';
  import { errorDialog, successDialog } from '../../../services/helpers';
  import TutorialSelection from '../parts/TutorialSelection';

  export default {
    mixins: [loadingMixin, pushToMixin],
    props: ['id'],
    components: {
      TutorialSelection,
      IDCard,
      SubmitButton,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      EditorFrame: () => import('../frames/EditorFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        editor: null,
        codeObject: {
          id: this.id,
          code: '',
          tutorial: '',
        },
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
      isCreatingNew() {
        return this.codeObject.id === newModelUUID;
      },
    },
    methods: {
      initCodeEditor() {
        import('monaco-editor')
          .then((md) => {
            this.editor = md.editor.create(document.getElementById('editor'), {
              fontSize: this.fontSize,
              foldingStrategy: 'indentation', // fold text by indentation
              automaticLayout: true, // auto resize
              overviewRulerBorder: false, // scroll bar no boarder
              scrollBeyondLastLine: false, // remove blank space at the end of the editor
              theme: this.dark ? 'vs-dark' : 'vs',
              language: 'python',
            });
          })
          .then(() => {
            this.editor.getModel().onDidChangeContent((_) => {
              this.codeObject.code = this.editor.getValue();
            });
            this.initCode();
          })
          .catch((err) => {
            errorDialog({
              message: `Cannot load monaco editor! ${err}`,
            });
          });
      },
      fetchCode() {
        if (!this.isCreatingNew) {
          this.startLoading();
          apiCaller(codeQuery, { id: this.codeObject.id })
            .then((data) => {
              if (!data || !('code' in data)) {
                throw Error('Invalid data returned.');
              }

              this.codeObject = {
                id: this.codeObject.id,
                code: data.code.code,
                tutorial: data.code.tutorial.id,
              };

              this.initCode();
            })
            .catch((err) => {
              errorDialog({
                message: `An error occurs during fetching code. ${err}`,
              });
            })
            .then(() => {
              this.finishedLoading();
            });
        }
      },
      postCode() {
        this.startLoading();
        apiCaller(updateCodeMutation, this.codeObject)
          .then((data) => {
            if (!data || !('updateCode' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.updateCode.success) {
              throw Error('Cannot update code for unknown reason!');
            }

            this.pushToNewPlace(data.updateCode.model.id);
            successDialog({
              message: 'Update Code Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during updating the code. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      initCode() {
        if (this.editor) {
          this.editor.setValue(this.codeObject.code);
        }
      },
      postExecJson() {
        //
      },
    },
    mounted() {
      this.initCodeEditor();
      this.fetchCode();
    },
    destroyed() {
      this.editor.dispose();
    },
  };
</script>
