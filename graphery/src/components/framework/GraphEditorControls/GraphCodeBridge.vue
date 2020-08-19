<script>
  import {
    errorDialog,
    notAvailableMessage,
    saveTextToClipboard,
    successDialog,
  } from '@/services/helpers';

  import { mapGetters } from 'vuex';

  import ResultJsonManager from '@/components/framework/GraphEditorControls/ResultJsonManager';

  export default {
    mixins: [ResultJsonManager],
    data() {
      return {};
    },
    computed: {
      ...mapGetters('graphs', ['getCurrentGraphId', 'getCurrentGraphObject']),
      ...mapGetters('code', ['getCurrentCodeId', 'getCurrentCodeObject']),
      currentGraphId: {
        set(d) {
          this.$store.dispatch('graphs/loadCurrentGraphId', d);
        },
        get() {
          return this.getCurrentGraphId;
        },
      },
      currentCodeId: {
        set(d) {
          this.$store.dispatch('code/loadCurrentCodeId', d);
        },
        get() {
          return this.getCurrentCodeId;
        },
      },
      currentJsonObject() {
        return this.getCurrentJsonObject({
          graphId: this.currentGraphId,
          codeId: this.currentCodeId,
        });
      },
      editorControlSliderPosition() {
        return this.resultJsonPositions[
          this.getIdFromGraphIdAndCodeId(
            this.currentGraphId,
            this.currentCodeId
          )
        ];
      },
      currentVarObject() {
        return this.currentJsonObject[this.editorControlSliderPosition];
      },
      editorControlSliderLength() {
        return this.currentJsonObject.length;
      },
    },
    methods: {
      onSliderChange(pos) {
        this.updateResultJsonPosition(pos);
      },
      onStepBack() {
        // TODO
      },
      onStepForward() {
        // TODO
      },
      onPushToCloudExec() {
        notAvailableMessage();
      },
      onPushToLocalExec() {
        notAvailableMessage();
      },
      checkEditorInitialized(showErrorDialog = false) {
        if (this.$refs.editorWrapper) {
          return this.$refs.editorWrapper;
        } else {
          if (showErrorDialog) {
            errorDialog({
              message: 'Editor is not initialized.',
            });
          }
          return undefined;
        }
      },
      onCopyCurrentCode() {
        const editorWrapper = this.checkEditorInitialized(true);
        if (editorWrapper) {
          saveTextToClipboard(editorWrapper.getCurrentCode());
        }
      },
      onPasteFromClipboard() {
        const editorWrapper = this.checkEditorInitialized(true);
        if (editorWrapper) {
          navigator.clipboard
            .readText()
            .then((text) => {
              editorWrapper.setCurrentCode(text);
              successDialog({
                message: 'Pasted code successfully',
              });
            })
            .catch((err) => {
              errorDialog({
                message: 'Failed to read clipboard contents. ' + err,
              });
            });
        }
      },
      onChangeVariableListOrientation() {
        const editorWrapper = this.checkEditorInitialized(true);
        if (editorWrapper) {
          editorWrapper.changeVariableListOrientation();
        }
      },
      onCallWorkSpace() {
        notAvailableMessage();
      },
    },
  };
</script>
