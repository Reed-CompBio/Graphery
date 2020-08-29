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
  import { mapState } from 'vuex';
  import { errorDialog } from '@/services/helpers';
  let monacoEditor;

  export default {
    props: {
      lang: {
        type: String,
        default: 'python',
      },
      wrapLine: {
        type: Boolean,
        default: false,
      },
      miniMapEnable: {
        type: Boolean,
        default: false,
      },
      loadingOverride: {
        type: Boolean,
        default: false,
      },
    },
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
      editorAndContentLoading() {
        return this.editor === null || this.loadingOverride;
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
                language: this.lang,
                wordWrap: this.wrap || this.wrapLine ? 'on' : 'off',
                minimap: {
                  enabled: this.miniMapEnable,
                },
                glyphMargin: true,
              }
            );
            this.editor.getModel().onDidChangeContent((_) => {
              const codeContent = this.editor.getValue();
              this.content = codeContent;
              this.$emit('editorContentChanged', codeContent);
            });

            this.editor.onDidScrollChange((event) => {
              this.$emit(
                'editorScrollChanged',
                event.scrollTop /
                  (this.editor.getScrollHeight() -
                    this.editor.getLayoutInfo().height)
              );
            });

            this.editor.layout();
            this.$emit('editorInstanceLoaded');
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
        if (this.editor) {
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
