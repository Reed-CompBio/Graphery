<template>
  <div>
    <q-dialog v-model="show" persistent seamless position="bottom">
      <q-card class="popup-wrapper">
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
        <q-tab-panels animated class="tutorial-tab-panes" v-model="tab">
          <q-tab-panel name="code">
            <div id="editor-panel" :style="editorWrapperStyle">
              <div id="editor" :style="editorWrapperStyle"></div>
            </div>
          </q-tab-panel>
          <q-tab-panel name="info">
            <div id="info-panel">info</div>
          </q-tab-panel>
          <q-tab-panel name="settings">
            <div id="settings-panel">settings</div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
  import { editorTabHeight } from '@/store/states/meta.ts';
  let aceEdit;

  export default {
    props: ['show'],
    data() {
      return {
        tab: 'code',
        aceInstance: null,
      };
    },
    computed: {
      editorWrapperStyle() {
        return {
          height: `calc(40vh - ${editorTabHeight}px)`,
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
  .popup-wrapper
    min-width: 50vw
    min-height: 40vh
</style>
