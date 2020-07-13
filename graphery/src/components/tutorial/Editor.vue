<template>
  <div id="editor-panel">
    <q-resize-observer @resize="resizeAction"></q-resize-observer>
    <div id="editor" class="full-height"></div>
    <q-inner-loading :showing="editor === null || codesEmpty">
      <q-spinner-pie size="64px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
  import { mapGetters, mapState } from 'vuex';
  let monacoEditor;

  export default {
    data() {
      return {
        expanded: false,
        editor: null,
        content: '',
        decorations: [],
        sliderPos: 1,
      };
    },
    computed: {
      ...mapState('settings', [
        'dark',
        'enableEditing',
        'tabNum',
        'softTab',
        'fontSize',
        'wrap',
      ]),
      ...mapState('tutorials', ['codes']),
      ...mapGetters('tutorials', ['codesEmpty']),
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
                readOnly: !this.enableEditing,
                theme: this.dark ? 'vs-dark' : 'vs',
                language: 'python',
                minimap: {
                  enabled: false,
                },
                glyphMargin: true,
              }
            );
            console.debug('mounted monaco editor', this.editor);

            this.editor.setValue(this.codes);

            this.editor.layout();
          })
          .catch((err) => {
            // TODO setup popup
            console.error(
              'An error occurs when initializing the monaco code editor',
              err
            );
          });
      },
      generateDecoration(line, message) {
        if (monacoEditor) {
          return {
            range: new monacoEditor.Range(line, 1, line, 1),
            options: {
              isWholeLine: true,
              className: 'exec-line-box',
              glyphMarginClassName: 'exec-line-pointer',
              glyphMarginHoverMessage: message,
            },
          };
        }
        return null;
      },
      changeDecoration(...decoration) {
        if (this.editor && decoration) {
          this.decorations = this.editor.deltaDecorations(
            this.decorations,
            decoration
          );
        }
      },
      focusToLine(line) {
        if (this.editor) {
          this.editor.revealLine(line);
        }
      },
      moveToLine(line, message = 'Executing this line') {
        // TODO scroll into view
        this.changeDecoration(this.generateDecoration(line, message));
        this.focusToLine(line);
      },
      resizeAction() {
        if (this.editor) {
          this.editor.layout();
        }
      },
    },
    watch: {
      codes: function() {
        if (this.editor && this.codes) {
          this.editor.setValue(this.codes);
        }
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
