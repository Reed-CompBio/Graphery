<template>
  <div id="editor-container" :style="editorPos">
    <q-card class="popup-wrapper">
      <q-bar v-touch-pan.prevent.mouse="handlePanning">
        <q-icon name="mdi-function" />
        <div style="text-transform: uppercase;">{{ tab }}</div>
        <q-space />
        <!-- TODO  get the button actions done -->
        <q-btn-group flat class="q-mr-md" v-touch-pan.prevent.mouse="null">
          <q-btn dense>
            <q-icon name="mdi-cloud-upload" />
            <q-tooltip class="text-body1">
              {{ $t('tooltips.runCodeOnTheCloud') }}
            </q-tooltip>
          </q-btn>
          <q-btn dense>
            <q-icon name="mdi-play" />
            <q-tooltip class="text-body1">
              {{ $t('tooltips.runCodeLocally') }}
            </q-tooltip>
          </q-btn>
        </q-btn-group>
        <q-btn-group flat class="q-mr-md">
          <q-btn dense icon="mdi-content-copy">
            <q-tooltip class="text-body1">
              {{ $t('tooltips.copyCodes') }}
            </q-tooltip>
          </q-btn>
          <q-btn dense icon="mdi-content-paste">
            <q-tooltip class="text-body1">
              {{ $t('tooltips.pasteCodes') }}
            </q-tooltip>
          </q-btn>
        </q-btn-group>
        <q-btn
          dense
          flat
          icon="close"
          @click="closeWindow"
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
          <div id="editor-panel" :style="editorWrapperStyle">
            <div id="editor" :style="editorWrapperStyle"></div>
            <q-inner-loading :showing="codesEmpty">
              <q-spinner-pie size="64px" color="primary" />
            </q-inner-loading>
          </div>
        </q-tab-panel>
        <q-tab-panel name="info">
          <div id="info-panel">info</div>
        </q-tab-panel>
        <q-tab-panel name="settings">
          <!-- maybe I don't need this -->
          <div id="settings-panel">settings</div>
        </q-tab-panel>
        <q-tab-panel name="shortcuts">
          <div id="shortcuts-panel">shortcuts</div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </div>
</template>

<script>
  import { editorTabHeight } from '@/store/states/meta.ts';
  import { mapState, mapGetters } from 'vuex';
  let aceEdit;
  let Range;

  export default {
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
        require('brace/mode/python'); //language
        require('brace/theme/chrome');
        console.debug('acquired modules for ace editor');
      },
      closeWindow() {
        console.debug('close editor window');
        this.$emit('close-editor');
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
    },
    computed: {
      ...mapState('settings', ['tabNum', 'softTab', 'fontSize', 'wrap']),
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
      import('brace')
        .then((br) => {
          console.debug('brace (ace) editor module: ', br);

          aceEdit = br.edit;
          console.debug('ace edit func: ', aceEdit);

          this.editorInit();

          Range = br.acequire('ace/range').Range;

          this.aceInstance = aceEdit('editor');
          this.aceInstance.setOption({
            enableBasicAutocompletion: true, // the editor completes the statement when you hit Ctrl + Space
            enableLiveAutocompletion: true, // the editor completes the statement while you are typing
            showPrintMargin: false, // hides the vertical limiting strip
            maxLines: 500,
            fontSize: '100%', // ensures that the editor fits in the environment
          });

          this.aceInstance.getSession().setMode('ace/mode/python');
          this.aceInstance.setTheme('ace/theme/chrome');

          this.aceInstance.setValue(
            `def test():
   print('this is as test function')
  `
          );

          // this.aceInstance.addMarker(new Range(1, 0, 2, 0));
        })
        .catch((err) => {
          console.error(
            'An error occurs when initializing the code editor: ',
            err
          );
        });
    },
  };
</script>

<style lang="sass">
  #editor-container
    position: absolute
    z-index: 2001
  .popup-wrapper
    min-width: 50vw
    max-width: 900px
    min-height: 45vh
    max-height: 600px
</style>
