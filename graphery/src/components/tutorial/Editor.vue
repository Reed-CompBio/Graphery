<template>
  <div id="editor-panel" class="editor-light">
    <div id="editor" class="full-height"></div>
    <q-inner-loading :showing="editor === null">
      <q-spinner-pie size="64px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  let monacoEditor;

  export default {
    data() {
      return {
        editor: null,
        content: '',
        decorations: [],
      };
    },
    computed: {
      ...mapState('settings', [
        'dark',
        'tabNum',
        'softTab',
        'fontSize',
        'wrap',
      ]),
    },
    methods: {
      initMonacoEditor() {
        import('monaco-editor')
          .then((md) => {
            console.debug('monaco editor module: ', md);
            monacoEditor = md;

            // TODO store user edited code
            this.editor = monacoEditor.editor.create(
              document.getElementById('editor'),
              {
                fontSize: this.fontSize,
                foldingStrategy: 'indentation', // fold text by indentation
                automaticLayout: true, // auto resize
                overviewRulerBorder: false, // scroll bar no boarder
                scrollBeyondLastLine: false, // remove blank space at the end of the editor
                readOnly: false,
                theme: this.dark ? 'hc-black' : 'vs',
                language: 'python',
                minimap: {
                  enabled: false,
                },
                glyphMargin: true,
              }
            );
            console.debug('mounted monaco editor');

            // Set text to editor
            this.editor.setValue(
              ['def hello():', '\tprint("hello world :)")'].join('\n')
            );

            const decoration = {
              range: new monacoEditor.Range(2, 1, 2, 1),
              options: {
                isWholeLine: true,
                className: 'exec-line-box',
                glyphMarginClassName: 'exec-line-pointer',
                glyphMarginHoverMessage: 'Executing this line',
              },
            };
            this.decorations = this.editor.deltaDecorations(this.decorations, [
              decoration,
            ]);
          })
          .catch((err) => {
            console.error(
              'An error occurs when initializing the monaco code editor',
              err
            );
          });
      },
    },
    mounted() {
      this.initMonacoEditor();
    },
    destroyed() {
      this.editor.dispose();
    },
  };
</script>

<style lang="sass">
  @import "~@/styles/editor.sass"
</style>
