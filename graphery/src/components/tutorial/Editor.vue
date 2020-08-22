<template>
  <div id="editor-panel">
    <q-resize-observer @resize="resizeAction"></q-resize-observer>
    <div id="editor" class="full-height"></div>
    <q-inner-loading :showing="editorAndContentLoading">
      <q-spinner-pie size="64px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
  import { mapGetters, mapState } from 'vuex';
  import { errorDialog } from '@/services/helpers';
  let monacoEditor;

  export default {
    data() {
      return {
        expanded: false,
        editor: null,
        content: '',
        decorations: [],
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
      ...mapGetters('code', ['codeObjectListEmpty']),
      editorAndContentLoading() {
        return this.editor === null || this.codeObjectListEmpty;
      },
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
            this.editor.getModel().onDidChangeContent((_) => {
              const codeContent = this.editor.getValue();
              this.content = codeContent;
              this.$emit('editorContentChanged', codeContent);
            });
            console.debug('mounted monaco editor', this.editor);

            this.editor.setValue(this.codes);

            this.editor.layout();
          })
          .catch((err) => {
            errorDialog({
              message:
                'An error occurs when initializing the Monaco code editor. ' +
                err,
            });
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
        if (this.editor) {
          this.decorations = this.editor.deltaDecorations(
            this.decorations,
            decoration
          );
        }
      },
      clearDecoration() {
        this.changeDecoration();
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
      getCodeContent() {
        return this.content;
      },
      setCodeContent(content) {
        if (this.enableEditing) {
          this.editor.setValue(content);
        }
      },
    },
    mounted() {
      this.initMonacoEditor();
    },
    beforeDestroy() {
      if (this.editor) {
        this.editor.dispose();
      }
    },
  };
</script>

<style lang="sass">
  @import "~@/styles/editor.sass"
</style>
