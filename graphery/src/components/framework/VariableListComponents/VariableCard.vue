<template>
  <q-card>
    <VariableCardHeader
      :has-previous="!isStackEmpty"
      :init-element-name.sync="currentVariableName"
      :init-element.sync="currentVariableObject"
      :init-element-color="rootVariableColor"
      :init-toggle-state="toggleState"
      @popVariableStack="handlePopVariableStack"
      @toggleAction="handleToggleAction"
    ></VariableCardHeader>
    <q-separator />
    <VariableCardDisplay
      ref="variableCardDisplay"
      :init-element.sync="currentVariableObject"
      :init-root-element-name="rootVariableName"
      @clearHighlight="emitClearHighlight"
      @highlight="emitHighlight"
      @toggle="emitToggleHighlight"
      @pushVariableStack="handlePushVariableStack"
      @toggleStateChange="handleToggleStateChange"
      class="q-my-sm"
    ></VariableCardDisplay>
  </q-card>
</template>

<script>
  import VariableCardHeader from '@/components/framework/VariableListComponents/VariableCardHeader';
  import VariableCardDisplay from '@/components/framework/VariableListComponents/VariableCardDisplay';
  import {
    _COLOR_HEADER,
    _LABEL_HEADER,
    _PYTHON_ID_HEADER,
  } from '@/components/framework/VariableListComponents/variableListConstants';
  import { revertNameCombo } from '@/components/framework/GraphEditorControls/ElementsUtils';
  export default {
    props: {
      initVariableObject: {
        type: Object,
        default: null,
      },
    },
    components: { VariableCardDisplay, VariableCardHeader },
    data() {
      return {
        variableNameStack_: [],
        variableStack_: [],
        initVarColor_: null,
        toggleState_: 1,
      };
    },
    computed: {
      rootVariable() {
        return this.initVariableObject;
      },
      rootVariableName() {
        return revertNameCombo(this.initVariableObject[_LABEL_HEADER]);
      },
      variableStack() {
        return [this.rootVariable, ...this.variableStack_];
      },
      variableNameStack() {
        return [this.rootVariableName, ...this.variableNameStack_];
      },
      isStackEmpty() {
        return this.variableStack_.length === 0;
      },
      currentVariableObject() {
        return this.variableStack[this.variableStack.length - 1];
      },
      currentVariableName() {
        return this.variableNameStack.join('');
      },
      rootVariableColor() {
        return this.rootVariable[_COLOR_HEADER];
      },
      toggleState() {
        return this.toggleState_;
      },
    },
    methods: {
      resetVariableStacks() {
        this.variableStack_ = [];
        this.variableNameStack_ = [];
      },
      handlePopVariableStack() {
        if (this.variableStack.length > 1) {
          this.variableStack_.pop();
          this.variableNameStack_.pop();
        }
      },
      handlePushVariableStack(name, element) {
        if (typeof element === 'string' || element instanceof String) {
          for (let i = this.variableStack_.length - 1; i >= 0; i--) {
            if (element === this.variableStack_[i][_PYTHON_ID_HEADER]) {
              element = this.variableStack_[i];
              break;
            }
          }
        }
        this.variableStack_.push(element);
        this.variableNameStack_.push(name);
      },
      handleToggleAction() {
        this.$refs.variableCardDisplay.toggleVar(this.toggleState);
      },
      handleToggleStateChange(toggleStateChange) {
        this.toggleState_ = toggleStateChange;
      },
      resetToggleState() {
        this.toggleState_ = 1;
      },
      emitClearHighlight(bareClassName) {
        this.$emit('clearHighlightFromVarList', bareClassName);
      },
      emitHighlight(bareClassName, graphIds) {
        /**
         * if it's an element, highlight it, and toggle it
         * if it's a linear container, highlight all, toggle all
         * if it's a mapping container, highlight all, but only toggle key
         *
         * elements is in type of string
         */
        this.$emit(
          'highlightFromVarList',
          bareClassName,
          graphIds,
          this.rootVariableColor
        );
      },
      emitToggleHighlight(ids, className, flag) {
        /**
         * if it's singular or linear container, just on and off
         * if it's pair container, key on, value on, off
         */
        this.$emit('toggleHighlightFromVarList', ids, className, Boolean(flag));
      },
    },
    watch: {
      rootVariable: function() {
        this.resetVariableStacks();
      },
    },
  };
</script>
