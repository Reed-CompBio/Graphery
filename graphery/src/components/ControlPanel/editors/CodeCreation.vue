<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Code Editor
    </template>
    <template>
      <EditorFrame>
        <template v-slot:left>
          <q-card id="editor-wrapper" class="q-py-md q-px-sm">
            <div style="height: 70vh;" id="editor"></div>
          </q-card>
        </template>
        <template v-slot:right>
          <div id="tutorial-selection">
            <InfoCard>
              <template v-slot:title>
                Tutorial
              </template>
              <q-select
                label="Tutorial"
                v-model="tutorialChoice"
                :options="tutorialOptions"
                use-chips
                outlined
                dense
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

  export default {
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
      };
    },
    computed: {
      ...mapState('settings', ['dark', 'fontSize']),
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
