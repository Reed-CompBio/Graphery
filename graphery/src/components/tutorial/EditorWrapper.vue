<template>
  <div id="editor-container">
    <div class="row" style="height: calc(100% - 32px); overflow: hidden;">
      <q-splitter
        v-model="codeValueListSplitPos"
        :separator-class="
          variableListHorizontal
            ? 'resizable-h-separator-splitter'
            : 'resizable-v-separator-splitter'
        "
        :horizontal="variableListHorizontal"
        class="full-height full-width"
      >
        <template v-slot:before>
          <q-card class="popup-wrapper full-height" style="overflow-y: hidden;">
            <Editor
              ref="editorComponent"
              class="full-height"
              :loadingOverride="editorLoadingOverride"
              @editorContentChanged="emitEditorContentChanged"
              @editorInstanceLoaded.once="onEditorInstanceLoaded"
            ></Editor>
          </q-card>
        </template>
        <template v-slot:separator>
          <SplitterSeparator :horizontal="variableListHorizontal" />
        </template>
        <template v-slot:after>
          <VariableList></VariableList>
        </template>
      </q-splitter>
    </div>
    <!--    <q-dialog v-model="isWorkSpaceSelectionOpen">-->
    <!--      <q-card>-->
    <!--        <q-toolbar>-->
    <!--          <TutorialWorkSpaceController-->
    <!--            style="width: 30%"-->
    <!--            class="q-mr-md"-->
    <!--          ></TutorialWorkSpaceController>-->
    <!--          <q-space />-->
    <!--          <q-btn flat round dense icon="close" v-close-popup />-->
    <!--        </q-toolbar>-->

    <!--        <q-drawer :v-model="true" persistent bordered>-->
    <!--          <q-list>-->
    <!--            <q-item v-for="i in [1, 2, 3]" :key="i">-->
    <!--              {{ i }}-->
    <!--            </q-item>-->
    <!--          </q-list>-->
    <!--        </q-drawer>-->
    <!--        <q-card-section>-->
    <!--          Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum-->
    <!--          repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis-->
    <!--          perferendis totam, ea at omnis vel numquam exercitationem aut, natus-->
    <!--          minima, porro labore.-->
    <!--        </q-card-section>-->
    <!--      </q-card>-->
    <!--    </q-dialog>-->
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import { errorDialog } from '@/services/helpers';
  import Editor from '@/components/framework/Editor.vue';
  import pushCodeToLocalMixin from '@/components/mixins/PushCodeToLocalMixin';
  import VariableList from '@/components/tutorial/VariableList';
  import SplitterSeparator from '@/components/framework/SplitterSeparator';

  export default {
    mixins: [pushCodeToLocalMixin],
    props: {
      editorLoadingOverride: {
        type: Boolean,
        default: false,
      },
    },
    components: {
      SplitterSeparator,
      Editor,
      VariableList,
      // TODO decouple the workspace controller
      // TutorialWorkSpaceController: () =>
      //   import('@/components/tutorial/TutorialWorkSpaceController.vue'),
    },
    data() {
      return {
        sliderPos: 1,
        codeValueListSplitPos: (5 / 6) * 100,
      };
    },
    computed: {
      ...mapState('settings', ['variableListHorizontal']),
    },
    methods: {
      editorMoveLine(lineNumber) {
        this.$refs.editorComponent.moveToLine(lineNumber);
      },
      editorClearLineNumber() {
        // TODO
        this.$refs.editorComponent.clearnLine();
      },
      getEditorComponent(showErrorDialog = false) {
        if (this.$refs.editorComponent) {
          return this.$refs.editorComponent;
        } else {
          if (showErrorDialog) {
            errorDialog({
              message: 'Editor Element is not initialized.',
            });
          }
        }
      },
      getCurrentCode() {
        const editor = this.getEditorComponent();
        return editor ? editor.getCodeContent() : '';
      },
      setCurrentCode(code) {
        const editor = this.getEditorComponent();
        editor.setCodeContent(code);
      },
      clearEditorDecoration() {
        const editor = this.getEditorComponent();
        editor.clearDecoration();
      },
      changeVariableListOrientation() {
        this.$store.dispatch(
          'settings/changeVariableListOrientation',
          !this.variableListHorizontal
        );
      },
      emitEditorContentChanged(newCode) {
        this.$emit('editorContentChanged', newCode);
      },
      onEditorInstanceLoaded() {
        this.$emit('editorInstanceLoaded');
      },
    },
  };
</script>

<style lang="sass">
  .q-tab-panel
    padding: 8px
  #editor-container
    position: absolute
    z-index: auto
    height: 100% !important
    width: 100% !important
  #stepper-slider .q-slider__pin
    z-index: 10
</style>
