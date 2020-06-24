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
                foldingStrategy: 'indentation', // 代码可分小段折叠
                automaticLayout: true, // 自适应布局
                overviewRulerBorder: false, // 不要滚动条的边框
                scrollBeyondLastLine: false, // 取消代码后面一大段空白
                readOnly: false,
                theme: this.dark ? 'hc-black' : 'vs',
                language: 'python',
                minimap: {
                  enabled: false,
                  // TODO add an option here?
                },
              }
            );
            console.debug('mounted monaco editor');
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
