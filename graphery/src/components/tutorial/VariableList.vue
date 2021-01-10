<template>
  <div
    id="code-controller-wrapper"
    class="full-height full-width row flex-center"
  >
    <q-scroll-area
      class="fit q-px-sm"
      id="variable-list-scroll-area"
      :visible="false"
    >
      <VariableCard
        :key="index"
        v-for="(item, index) in variableDisplayList"
        :init-variable-object.sync="item"
        @clearHighlightFromVarList="emitClearHighlight"
        @highlightFromVarList="emitHighlight"
        @toggleHighlightFromVarList="emitToggleHighlight"
        class="q-my-md, q-py-sm q-px-md text-center"
      ></VariableCard>
      <VariableCard
        v-for="(item, index) in accessedVariableDisplayList"
        :key="index"
        :init-variable-object.sync="item"
        @clearHighlightFromVarList="emitClearHighlight"
        @highlightFromVarList="emitHighlight"
        @toggleHighlightFromVarList="emitToggleHighlight"
        class="q-my-md q-py-sm q-px-md text-center"
      ></VariableCard>
    </q-scroll-area>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';
  import {
    _ACCESSED_VARIABLE_OBJ_LABEL,
    _EMPTY_VALUE_STRING,
  } from '@/components/framework/VariableListComponents/variableListConstants';
  import VariableCard from '@/components/framework/VariableListComponents/VariableCard';

  const _EMPTY_VARIABLE_LIST_OBJ = [
    {
      label: 'Status',
      value: _EMPTY_VALUE_STRING,
    },
  ];

  export default {
    components: { VariableCard },
    props: ['variableObject'],
    computed: {
      ...mapGetters('variables', [
        'getCurrentVariables',
        'currentVariablesEmpty',
        'getCurrentAccessedVariables',
        'currentAccessedVariableEmpty',
      ]),
      currentVariables() {
        return this.getCurrentVariables;
      },
      variableDisplayList() {
        if (this.currentVariablesEmpty) {
          return _EMPTY_VARIABLE_LIST_OBJ;
        }

        const variableList = [];

        for (const [key, value] of Object.entries(this.currentVariables)) {
          variableList.push(this.processVariableElement(key, value));
        }
        return variableList;
      },
      currentAccessedVariables() {
        return this.getCurrentAccessedVariables;
      },
      accessedVariableDisplayList() {
        const accessedVariableList = [];

        if (this.currentAccessedVariableEmpty) {
          return accessedVariableList;
        }

        for (const value of this.currentAccessedVariables) {
          accessedVariableList.push(
            this.processVariableElement(_ACCESSED_VARIABLE_OBJ_LABEL, value)
          );
        }

        return accessedVariableList;
      },
    },
    methods: {
      processVariableElement(key, value) {
        return {
          label: key,
          ...value,
        };
      },
      emitClearHighlight() {
        this.$emit('clearHighlightFromVarList', this.rootVariableName);
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
          this.rootVariableName,
          graphIds,
          this.rootVariableColor
        );
      },
      emitToggleHighlight(elements, flag) {
        // TODO process states here
        /**
         * if it's singular or linear container, just on and off
         * if it's pair container, key on, value on, off
         */
        this.$emit('toggleHighlightFromVarList', elements, flag);
      },
    },
  };
</script>

<style lang="sass">
  #variable-list-scroll
      width: 90%
      vertical-align: middle
  .mock-h6
    font-size: 1.25rem
    font-weight: 500
    line-height: 2rem
    letter-spacing: 0.0125em
    text-wrap: normal
</style>
