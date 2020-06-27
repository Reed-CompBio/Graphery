<template>
  <div id="editor-panel" style="overflow-y: auto;">
    <div id="result-wrapper" style="z-index: auto;" class="q-mx-sm">
      <q-expansion-item :value="expanded" dense>
        <div class="q-mx-md">
          <q-slider
            v-model="sliderPos"
            :min="1"
            label
            :max="sliderLength"
            :step="1"
            dense
            :disable="disableStepSlider"
          ></q-slider>
          <q-virtual-scroll
            virtual-scroll-horizontal
            :items="variableDisplayList"
          >
            <template v-slot="{ item, index }">
              <div :key="index" :class="item.class">
                #{{ index }} - {{ item }}
              </div>
            </template>
          </q-virtual-scroll>
        </div>
      </q-expansion-item>

      <!--      <q-slider></q-slider>-->
    </div>
    <!--    style="height: calc(100% - 48px)"-->
    <!--    TODO fix height -->
    <div id="editor" style="height: calc(100% - 50px)"></div>
    <q-inner-loading :showing="editor === null">
      <q-spinner-pie size="64px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';
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
      ...mapState('tutorials', ['resultJson', 'variableObj']),
      ...mapGetters('tutorials', ['resultJsonEmpty', 'variableObjEmpty']),
      resultObject() {
        if (this.resultJsonEmpty) {
          return [];
        }
        return JSON.parse(this.resultJson);
      },
      sliderLength() {
        if (this.resultObject) {
          return this.resultObject.length + 1;
        }
        return 1;
      },
      disableStepSlider() {
        return this.sliderLength === 1;
      },
      variableDisplayList() {
        if (this.variableObjEmpty) {
          return [
            {
              label: 'Status',
              value: 'Empty',
            },
          ];
        }
        const variableList = [];
        for (const [key, value] of Object.entries(this.variableObj)) {
          let variableValue;
          if (typeof value === 'object') {
            variableValue = value['name'];
          } else {
            variableValue = value;
          }
          variableList.push({
            label: key.split('#').join('.'),
            value: variableValue,
          });
        }
        return variableList;
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

            // load text to editor
            this.editor.setValue(
              ['def hello():', '\tprint("hello world :)")'].join('\n')
            );
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
        this.changeDecoration(this.generateDecoration(line, message));
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
