<template>
  <div id="editor-container" :style="editorPos">
    <q-resize-observer @resize="resizePos"></q-resize-observer>
    <!--    <q-dialog :value="show" persistent seamless position="bottom">-->

    <q-card class="popup-wrapper">
      <q-bar v-touch-pan.prevent.mouse="handlePanning">
        <q-icon name="mdi-function" />
        <div style="text-transform: uppercase;">{{ tab }}</div>
        <q-space />
        <q-btn-group flat class="q-mr-md">
          <q-btn dense>
            <q-icon name="mdi-play"></q-icon>
          </q-btn>
        </q-btn-group>
        <q-btn dense flat icon="close" @click="closeWindow" />
      </q-bar>
      <q-tabs inline-label class="tutorial-tabs" v-model="tab">
        <q-tab name="code" icon="mdi-code-braces" label="code" />
        <q-tab name="info" icon="mdi-information-variant" label="info" />
        <q-tab
          name="settings"
          icon="mdi-card-bulleted-settings"
          label="settings"
        />
      </q-tabs>
      <q-separator />
      <q-tab-panels
        animated
        keep-alive
        class="tutorial-tab-panes"
        v-model="tab"
      >
        <q-tab-panel name="code">
          <div id="editor-panel" :style="editorWrapperStyle">
            <!--            <div id="editor" :style="editorWrapperStyle"></div>-->
            <editor
              v-model="content"
              @init="editorInit"
              lang="html"
              theme="chrome"
              width="500"
              height="100"
              ref="editor"
              :style="editorWrapperStyle"
            ></editor>
            <!--            <editor :style="editorWrapperStyle"></editor>-->
          </div>
        </q-tab-panel>
        <q-tab-panel name="info">
          <div id="info-panel">info</div>
        </q-tab-panel>
        <q-tab-panel name="settings">
          <!-- maybe I don't need this -->
          <div id="settings-panel">settings</div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
    <!--    </q-dialog>-->
  </div>
</template>

<script>
  import { editorTabHeight } from '@/store/states/meta.ts';
  let aceEdit;

  export default {
    components: {
      editor: () => import('vue2-ace-editor'),
    },
    data() {
      return {
        tab: 'code',
        aceInstance: null,
        content: '',
        isPanning: false,
        pos: {
          x: window.innerWidth / 4,
          y: window.innerHeight * 0.275,
        },
      };
    },
    methods: {
      editorInit: function() {
        require('brace/ext/language_tools'); //language extension prerequsite...
        require('brace/mode/html');
        require('brace/mode/python'); //language
        require('brace/mode/less');
        require('brace/theme/chrome');
        require('brace/snippets/javascript'); //snippet
      },
      closeWindow() {
        console.debug('close editor window');
        this.$emit('close-editor');
      },
      handlePanning({ delta }) {
        this.pos.x += delta.x;
        this.pos.y += delta.y;
      },
      resizePos() {
        this.pos = {
          x: window.innerWidth / 4,
          y: window.innerHeight * 0.275,
        };
      },
    },
    computed: {
      editorWrapperStyle() {
        return {
          height: `calc(40vh - ${editorTabHeight}px)`,
        };
      },
      editorPos() {
        return {
          top: `${this.pos.y}px`,
          left: `${this.pos.x}px`,
        };
      },
    },
    mounted() {
      // import('ace-builds')
      //   .then((ac) => {
      //     // Object.freeze(document.getElementById('editor'));
      //
      //     console.debug('ace code editor module: ', ac);
      //     ac.config.set('basePath', '/ace-builds/src-noconflict');
      //     ac.config.set('modePath', '/ace-builds/src-noconflict');
      //     ac.config.set('themePath', '/ace-builds/src-noconflict');
      //     aceEdit = ac.edit;
      //     console.debug('ace edit func: ', aceEdit);
      //
      //     this.aceInstance = aceEdit('editor');
      //     this.aceInstance.setOptions({
      //       enableBasicAutocompletion: true, // the editor completes the statement when you hit Ctrl + Space
      //       enableLiveAutocompletion: true, // the editor completes the statement while you are typing
      //       showPrintMargin: false, // hides the vertical limiting strip
      //       maxLines: 500,
      //       fontSize: '100%', // ensures that the editor fits in the environment
      //     });
      //
      //     // this.aceInstance.getSession().setUseWorker(false);
      //
      //     // this.aceInstance.setTheme('ace/theme/monokai');
      //     // this.aceInstance.getSession().setMode('ace/mode/python');
      //
      //     console.debug('ace editor instance: ', this.aceInstance);
      //   })
      //   .catch((err) => {
      //     console.error(err);
      //   });
    },
  };
</script>

<style lang="sass">
  #editor-container
    position: absolute
    /*top: 27.5vh*/
    /*left: 25vw*/
    z-index: 10000

  .popup-wrapper
    min-width: 50vw
    min-height: 45vh
</style>
