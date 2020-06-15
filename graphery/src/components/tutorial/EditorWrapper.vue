<template>
  <div id="editor-container" :style="editorPos">
    <q-card class="popup-wrapper" v-show="editorShow">
      <q-bar v-touch-pan.prevent.mouse="handlePanning">
        <q-icon name="mdi-function" />
        <div style="text-transform: uppercase;">{{ tab }}</div>
        <q-space />
        <!-- TODO  get the button actions done -->
        <q-btn-group flat class="q-mr-md" v-touch-pan.prevent.mouse="null">
          <q-btn dense>
            <q-icon name="mdi-cloud-upload" />
            <SwitchTooltip
              :text="$t('tooltips.runCodeOnTheCloud')"
            ></SwitchTooltip>
          </q-btn>
          <q-btn dense>
            <q-icon name="mdi-play" />
            <SwitchTooltip
              :text="$t('tooltips.runCodeLocally')"
            ></SwitchTooltip>
          </q-btn>
        </q-btn-group>
        <q-btn-group flat class="q-mr-md">
          <q-btn dense icon="mdi-content-copy">
            <SwitchTooltip :text="$t('tooltips.copyCodes')"></SwitchTooltip>
          </q-btn>
          <q-btn dense icon="mdi-content-paste">
            <SwitchTooltip :text="$t('tooltips.pasteCodes')"></SwitchTooltip>
          </q-btn>
        </q-btn-group>
        <q-btn
          dense
          flat
          icon="close"
          @click="closeEditor"
          v-touch-pan.prevent.mouse="null"
        />
      </q-bar>
      <q-tabs dense inline-label class="tutorial-tabs" v-model="tab">
        <q-tab name="code" icon="mdi-code-braces" label="code" />
        <q-tab name="info" icon="mdi-information-variant" label="info" />
        <q-tab
          name="settings"
          icon="mdi-card-bulleted-settings"
          label="settings"
        />
        <q-tab
          name="shortcuts"
          icon="mdi-format-list-bulleted"
          label="shortcuts"
        >
        </q-tab>
      </q-tabs>
      <q-separator />
      <q-tab-panels
        animated
        keep-alive
        class="tutorial-tab-panes"
        v-model="tab"
      >
        <q-tab-panel name="code">
          <div
            id="editor-panel"
            class="editor-light"
            :style="editorWrapperStyle"
          >
            <div id="editor" :style="editorWrapperStyle"></div>
            <q-inner-loading :showing="editor === null">
              <q-spinner-pie size="64px" color="primary" />
            </q-inner-loading>
          </div>
        </q-tab-panel>
        <q-tab-panel name="info">
          <!-- TODO fill in info section -->
          <div id="info-panel">info</div>
        </q-tab-panel>
        <q-tab-panel name="settings">
          <!-- TODO maybe I don't need this -->
          <div id="settings-panel">settings</div>
        </q-tab-panel>
        <q-tab-panel name="shortcuts">
          <!-- TODO fill in shortcuts section -->
          <div id="shortcuts-panel">shortcuts</div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
    <q-page-sticky
      v-if="$q.screen.gt.xs"
      position="bottom-left"
      :offset="[30, 30]"
    >
      <SwitchTooltip :text="$t('tooltips.showEditorAndMore')"></SwitchTooltip>
      <q-btn round color="primary" icon="mdi-code-json" @click="toggleEditor" />
    </q-page-sticky>
  </div>
</template>

<script>
  import { editorTabHeight } from '@/store/states/meta.ts';
  import { mapState, mapGetters } from 'vuex';
  let aceEditor;
  let Range;
  let monacoEditor;

  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
    },
    data() {
      return {
        editorShow: true,
        tab: 'code',
        editor: null,
        content: '',
        isPanning: false,
        pos: {
          x: window.innerWidth / 4,
          y: window.innerHeight * 0.275,
        },
      };
    },
    methods: {
      toggleEditor() {
        this.editorShow = !this.editorShow;
      },
      closeEditor() {
        this.editorShow = false;
      },
      editorInit: function() {
        require('brace/ext/language_tools'); //language extension prerequsite...
        require('brace/mode/python'); //language
        require('brace/theme/chrome');
        console.debug('acquired modules for ace editor');
      },
      handlePanning({ delta }) {
        this.pos.x += delta.x;
        this.pos.y += delta.y;
      },
      resizeEditorPos() {
        this.pos = {
          x: window.innerWidth / 4,
          y: window.innerHeight * 0.275,
        };
      },
      initAceEditor() {
        import('brace')
          .then((br) => {
            console.debug('brace (ace) editor module: ', br);

            aceEditor = br.edit;
            console.debug('ace edit func: ', aceEditor);

            this.editorInit();

            Range = br.acequire('ace/range').Range;

            this.editor = aceEditor('editor');
            this.editor.setOption({
              enableBasicAutocompletion: true, // the editor completes the statement when you hit Ctrl + Space
              enableLiveAutocompletion: true, // the editor completes the statement while you are typing
              showPrintMargin: false, // hides the vertical limiting strip
              maxLines: 500,
              fontSize: '100%', // ensures that the editor fits in the environment
            });

            this.editor.getSession().setMode('ace/mode/python');
            this.editor.setTheme('ace/theme/chrome');

            this.editor.setValue(
              `def test():
   print('this is as test function')
  `
            );

            // this.aceInstance.addMarker(new Range(1, 0, 2, 0));
          })
          .catch((err) => {
            console.error(
              'An error occurs when initializing the ace code editor: ',
              err
            );
          });
      },
      initMonacoEditor() {
        import('monaco-editor')
          .then((md) => {
            console.debug('monaco editor module: ', md);
            monacoEditor = md;

            this.editor = monacoEditor.editor.create(
              document.getElementById('editor'),
              {
                fontSize: this.fontSize,
                foldingStrategy: 'indentation', // 代码可分小段折叠
                automaticLayout: true, // 自适应布局
                overviewRulerBorder: false, // 不要滚动条的边框
                language: 'python',
                theme: this.dark ? 'hc-black' : 'vs',
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
    computed: {
      ...mapState('settings', [
        'dark',
        'tabNum',
        'softTab',
        'fontSize',
        'wrap',
      ]),
      ...mapGetters('tutorials', ['codesEmpty']),
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
      // console.log(monaco);
      this.initMonacoEditor();
    },
  };
</script>

<style scoped lang="sass">
  #editor-container
    position: absolute
    z-index: 2001
  .popup-wrapper
    min-width: 50vw
    max-width: 900px
    min-height: 45vh
    max-height: 600px
</style>
