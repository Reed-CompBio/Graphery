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
  import PushCodeToLocalMixin from '@/components/mixins/PushCodeToLocalMixin';
  import PushCodeToCloudMixin from '@/components/mixins/PushCodeToCloudMixin';
  import { VARIABLE_EMPTY_CONTENT_NOTATION } from '@/components/framework/GraphEditorControls/parameters';

  export default {
    mixins: [
      ResultJsonManager,
      CodeManager,
      GraphManager,
      PushCodeToLocalMixin,
      PushCodeToCloudMixin,
    ],
    data() {
      return {
        loadedList: {
          editor: false,
          cytoscape: false,
        },
      };
    },
    computed: {
      execLoading() {
        return this.isExecutingLocally || this.isExecutingRemotely;
      },
      editorControlSliderPosition() {
        return this.getResultJsonPositionObject(this.currentPositionId);
      },
      editorControlSliderLength() {
        return this.currentJsonObject
          ? this.currentJsonObject.jsonObject.length || 1
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
            return [element, i];
          }
          // which should never happen
        }
        // return number
      },
      singleStep(element) {
        // element: {line: number, variables: object}

        if (!this.emptyVariables(element)) {
          this.viewUpdater(element, true);
        }
      },
      multipleSteps(noneEmptyElement, updateAccessed) {
        this.viewUpdater(noneEmptyElement, updateAccessed);
      },
      highlightVariablesOnCytoscapeView(variables) {
        if (this.$refs.cytoscapeWrapper) {
          this.$refs.cytoscapeWrapper.highlightVarObj(variables);
        }
      },
      highlightAccessedVariablesOnCytoscapeView(accessedVariables) {
        if (this.$refs.cytoscapeWrapper) {
          this.$refs.cytoscapeWrapper.highlightAccessedVariables(
            accessedVariables
          );
        }
      },
      unhighlightAccessedVariablesOnCytoscapeView() {
        if (this.$refs.cytoscapeWrapper) {
          this.$refs.cytoscapeWrapper.unhighlightAccessedVariables();
        }
      },
      updateVariableList(variables) {
        this.$store.commit('variables/LOAD_CURRENT_VARIABLES', variables);
      },
      updateAccessedVariables(accessedVariables) {
        this.$store.commit(
          'variables/LOAD_CURRENT_ACCESSES',
          accessedVariables
        );
      },
      clearAccessedVariables() {
        this.$store.commit('variables/CLEAR_CURRENT_ACCESSES');
      },
      viewUpdater(element, updateAccessed) {
        // elements: non null
        if (updateAccessed) {
          // update accessed variables
          const accessedVariables = element['accesses'];
          this.updateAccessedVariables(accessedVariables);
          this.highlightAccessedVariablesOnCytoscapeView(accessedVariables);
        } else {
          // clear accessed variables
          this.clearAccessedVariables();
          this.unhighlightAccessedVariablesOnCytoscapeView();
        }

        const variables = element['variables'];
        this.updateVariableList(variables);
        this.highlightVariablesOnCytoscapeView(variables);
      },
      stepper(newPosition, steps) {
        this.updateResultJsonPosition(this.currentPositionId, newPosition);
        const element = this.getResultJsonObjectElement(
          { graphId: this.currentGraphId, codeId: this.currentCodeId },
          newPosition
        );

        if (!element) {
          return;
        }

        this.updateEditorLine(element['line']);

        if (steps === 1) {
          this.singleStep(element);
        } else {
          const [
            noneEmptyElement,
            searchedPos,
          ] = this.findLastNoneEmptyElementPos(newPosition);
          this.multipleSteps(noneEmptyElement, searchedPos === newPosition);
        }
      },
      restartWithNewPosition(pos) {
        if (pos !== undefined) {
          this.$refs.editorControlUnit.setPositionValueCopyFromJsonPos(pos);
          this.stepper(pos, pos);
        }
      },
      resetContent() {
        const newPosition = this.getResultJsonPositionFromId(
          this.currentPositionId
        );
        this.restartWithNewPosition(newPosition);
      },
      updateResultJsonObject(obj) {
        this.$store.commit('rj/CHANGE_RESULT_JSON_OBJECT', {
          jsonObject: obj,
          graphId: this.currentGraphId,
          codeId: this.currentCodeId,
        });
      },
      updateResultJsonString(resultString) {
        this.$store.commit('rj/CHANGE_RESULT_JSON_STRING', {
          json: resultString,
          graphId: this.currentGraphId,
          codeId: this.currentCodeId,
        });
      },
      onExecuted(data) {
        if (PushCodeToCloudMixin.methods.onExecuted.call(this, data)) {
          this.updateResultJsonObject(data.data.execResult);
          this.updateResultJsonString(JSON.stringify(data.data.execResult));
          successDialog({
            message: 'Executed Successfully',
          });
          this.finishedCloudExecution();
        }
      },
      onPushToCloudExec() {
        this.restartWithNewPosition(0);
        this.sendDataToCloudExecutor(
          this.getCurrentCodeContent,
          this.getCurrentGraphId
        );
      },
      onPushToLocalExec() {
        const editorWrapper = this.checkEditorInitialized(true);

        if (editorWrapper) {
          this.pushToLocal(
            editorWrapper.getCurrentCode(),
            this.$store.getters['graphs/autoGeneratedCurrentGraphJsonObj'],
            () => {
              this.restartWithNewPosition(0);
            },
            (codeHash, execResult) => {
              this.updateResultJsonObject(execResult);
              this.updateResultJsonString(JSON.stringify(execResult));
            },
            () => null
          );
        }
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
      onEditorInstanceLoaded() {
        this.loadedList.editor = true;
        this.$refs.editorWrapper.setCurrentCode(this.getCurrentCodeContent);
      },
      onCytoscapeInstanceLoaded() {
        this.loadedList.cytoscape = true;
      },
    },
    watch: {
      currentJsonArr: function() {
        this.resetContent();
      },
      getCurrentCodeObject: function() {
        if (this.$refs.editorWrapper) {
          this.$refs.editorWrapper.clearEditorDecoration();
          this.$refs.editorWrapper.setCurrentCode(this.getCurrentCodeContent);
          this.resetContent();
        }
      },
    },
    destroyed() {
      this.$store.dispatch('rj/CLEAR_ALL');
      this.$store.dispatch('graphs/CLEAR_ALL');
      this.$store.dispatch('code/CLEAR_ALL');
      this.$store.dispatch('variables/CLEAR_ALL');
    },
  };
</script>
