<template>
  <div id="editor-container" :style="editorPos">
    <q-resize-observer @resize="resizePos"></q-resize-observer>
    <!--    <q-dialog :value="show" persistent seamless position="bottom">-->

    <q-card class="popup-wrapper">
      <q-bar v-touch-pan.prevent.mouse="handlePanning">
        <q-icon name="mdi-function" />
        <div style="text-transform: uppercase;">{{ tab }}</div>
        <q-space />
        <q-btn-group>
          <q-btn>
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
            <div id="editor" :style="editorWrapperStyle"></div>
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
    data() {
      return {
        tab: 'code',
        aceInstance: null,
        isPanning: false,
        pos: {
          x: window.innerWidth / 4,
          y: window.innerHeight * 0.275,
        },
      };
    },
    methods: {
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
      import('ace-builds')
        .then((ac) => {
          console.debug('ace code editor module: ', ac);
          aceEdit = ac.edit;
          console.debug('ace edit func: ', aceEdit);

          this.aceInstance = aceEdit('editor');
          // this.aceInstance.setTheme('ace/theme/monokai');
          // this.aceInstance.session.setMode('ace/mode/python');

          console.debug('ace editor instance: ', this.aceInstance);
        })
        .catch((err) => {
          console.error(err);
        });
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
