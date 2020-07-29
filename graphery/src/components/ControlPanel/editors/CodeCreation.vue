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
      <JsonCreation :code-id="codeObject.id" />
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
  import JsonCreation from './JsonCreation';

  export default {
    mixins: [loadingMixin, pushToMixin],
    props: ['id'],
    components: {
      JsonCreation,
      TutorialSelection,
      IDCard,
      SubmitButton,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      EditorFrame: () => import('../frames/EditorFrame.vue'),
    },
    data() {
      return {
        editor: null,
        codeObject: {
          id: this.id,
          code: '',
          tutorial: '',
        },
      };
    },
    computed: {
      ...mapState('settings', ['dark', 'fontSize']),
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

            this.codeObject.id = data.updateCode.model.id;

            this.pushToNewPlace(this.codeObject.id);
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
