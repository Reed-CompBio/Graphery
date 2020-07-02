<template>
  <div id="editor-panel">
    <q-resize-observer @resize="resizeAction"></q-resize-observer>
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
                theme: this.dark ? 'vs-dark' : 'vs',
                language: 'python',
                minimap: {
                  enabled: false,
                },
                glyphMargin: true,
              }
            );
            console.debug('mounted monaco editor');

            // load text to editor
            this.editor.setValue(
              'from supply import graph_obj as graph\n' +
                'from bundle.seeker import tracer\n' +
                '\n' +
                '\n' +
                "@tracer('edge', 'node', 'degree_dict')\n" +
                'def graphery_count_degree_by_edges() -> None:\n' +
                '    degree_dict = {}\n' +
                '\n' +
                '    for edge in graph.edges:\n' +
                '        for node in edge:\n' +
                '            if node in degree_dict:\n' +
                '                degree_dict[node] += 1\n' +
                '            else: \n' +
                '                degree_dict[node] = 1\n'
            );

            this.editor.layout();
            // TODO respond to splitter resize
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
        return {
          range: new monacoEditor.Range(line, 1, line, 1),
          options: {
            isWholeLine: true,
            className: 'exec-line-box',
            glyphMarginClassName: 'exec-line-pointer',
            glyphMarginHoverMessage: message,
          },
        };
      },
      changeDecoration(...decoration) {
        this.decorations = this.editor.deltaDecorations(
          this.decorations,
          decoration
        );
      },
      moveToLine(line, message = 'Executing this line') {
        // TODO scroll into view
        this.changeDecoration(this.generateDecoration(line, message));
      },
      resizeAction() {
        if (this.editor) {
          this.editor.layout();
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
