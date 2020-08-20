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
  import { VARIABLE_EMPTY_CONTENT_NOTATION } from '@/components/framework/GraphEditorControls/parameters';

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
      currentJsonArr() {
        return this.currentJsonObject && this.currentJsonObject.jsonObject;
      },
      currentPositionId() {
        return this.getIdFromGraphIdAndCodeId(
          this.currentGraphId,
          this.currentCodeId
        );
      },
      editorControlSliderPosition() {
        return this.getResultJsonPositionObject(this.currentPositionId);
      },
      editorControlSliderLength() {
        return this.currentJsonObject || this.currentJsonObject === []
          ? this.currentJsonObject.jsonObject.length
          : 1;
      },
    },
    methods: {
      emptyVariables(element) {
        return element['variables'] === VARIABLE_EMPTY_CONTENT_NOTATION;
      },
      onSliderChange(newPosition) {
        const positionDelta =
          newPosition -
          this.getResultJsonPositionFromId(this.currentPositionId);
        this.stepper(newPosition, positionDelta);
        // this.updateResultJsonPosition(this.currentPositionId, pos);
      },
      updateEditorLine(lineNumber) {
        if (this.$refs.editorWrapper) {
          this.$refs.editorWrapper.editorMoveLine(lineNumber);
        }
      },
      findLastNoneEmptyElementPos(pos) {
        // pos: number
        for (let i = pos; i >= 0; i--) {
          const element = this.getResultJsonObjectElement(
            { graphId: this.currentGraphId, codeId: this.currentCodeId },
            i
          );
          if (!this.emptyVariables(element)) {
            return element;
            // TODO what's the first element?
          }
        }
        // return number
      },
      singleStep(element) {
        // element: {line: number, variables: object}

        if (!this.emptyVariables(element)) {
          // TODO is the first element null?
          // has content, change update the graph and change editor highlight
          // TODO cytoscape interface
          // this.$refs.cytoscapeWrapper.highlightVarObj(element['variables']);
          // TODO update variable list
        }
      },
      multipleSteps(noneEmptyElement) {
        // TODO cytoscape interface
        // TODO update variable list
      },
      stepper(newPosition, steps) {
        console.log('stepper new position', newPosition);
        this.updateResultJsonPosition(this.currentPositionId, newPosition);
        const element = this.getResultJsonObjectElement(
          { graphId: this.currentGraphId, codeId: this.currentCodeId },
          newPosition
        );
        this.updateEditorLine(element['line']);

        if (steps === 1 || steps === -1) {
          console.log('stepper element', element);
          this.singleStep(element);
        } else {
          const noneEmptyElement = this.findLastNoneEmptyElementPos(
            newPosition
          );
          console.log('none empty element', noneEmptyElement);
          this.multipleSteps(noneEmptyElement);
        }
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
    watch: {
      //
    },
  };
</script>
