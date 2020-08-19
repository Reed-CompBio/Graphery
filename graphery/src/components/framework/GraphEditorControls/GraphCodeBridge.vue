<script>
  import {
    errorDialog,
    notAvailableMessage,
    saveTextToClipboard,
    successDialog,
  } from '@/services/helpers';
  import ResultJsonManager from '@/components/framework/GraphEditorControls/ResultJsonManager';
  import CodeManager from '@/components/framework/GraphEditorControls/CodeManager';
  import GraphManager from '@/components/framework/GraphEditorControls/GraphManager';

  export default {
    mixins: [ResultJsonManager, CodeManager, GraphManager],
    data() {
      return {};
    },
    computed: {
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
        return this.currentCodeObject ? this.currentCodeObject.length : 1;
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
      onEditorContentChanged(newCode) {
        this.updateCode(newCode);
      },
    },
  };
</script>
