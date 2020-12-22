<!-- TODO use pop up edit? -->
<template>
  <div id="code-controller-wrapper" class="full-height row flex-center">
    <q-virtual-scroll
      class="full-height"
      :items="variableDisplayList"
      id="variable-list-scroll"
    >
      <!-- make cards wrap when the width is enough -->
      <template v-slot="{ item, index }">
        <q-card :key="index" class="q-my-md q-py-sm q-px-md text-center">
          <div class="mock-h6" :style="`background-color: ${item.color}`">
            {{ item.label }}
          </div>
          {{ item.value }}
        </q-card>
      </template>
    </q-virtual-scroll>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';
  import { EMPTY_VARIABLE_ELEMENT_DISPLAY } from '@/components/framework/GraphEditorControls/parameters';
  import {
    isContainerElement,
    isGraphElement,
    isInitElement,
    isSingularElement,
    revertNameCombo,
  } from '@/components/framework/GraphEditorControls/ElementsUtils';

  const _EMPTY_VALUE_STRING = '<EMPTY>';

  const _EMPTY_VARIABLE_LIST_OBJ = [
    {
      label: 'Status',
      value: _EMPTY_VALUE_STRING,
    },
  ];

  const _ACCESSED_VARIABLE_OBJ_LABEL = 'Accessed';

  const _EMPTY_ACCESSED_VARIABLE_LIST_OBJ = [
    {
      label: _ACCESSED_VARIABLE_OBJ_LABEL,
      value: _EMPTY_VALUE_STRING,
    },
  ];

  export default {
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
        if (this.currentAccessedVariableEmpty) {
          return _EMPTY_ACCESSED_VARIABLE_LIST_OBJ;
        }

        const accessedVariableList = [];

        for (const value of this.currentAccessedVariables) {
          accessedVariableList.push(
            this.processVariableElement(_ACCESSED_VARIABLE_OBJ_LABLE, value)
          );
        }

        return accessedVariableList;
      },
    },
    methods: {
      revertGraphObject(nameCombo, element) {
        return {
          // TODO temporary work round figure out how to style it
          label: revertNameCombo(nameCombo),
          color: element['color'],
          value: element['repr'],
        };
      },
      revertNormalObject(nameCombo, element) {
        return {
          label: revertNameCombo(nameCombo),
          color: undefined,
          value: element['repr'],
        };
      },
      emptyObject(nameCombo) {
        return {
          label: revertNameCombo(nameCombo),
          color: undefined,
          value: EMPTY_VARIABLE_ELEMENT_DISPLAY,
        };
      },
      processVariableElement(key, value) {
        /**
         * Process individual variable, which is a object that follows the following protocol
         * {
         *   type: string
         *   color: string | null
         *   repr: string
         *   properties: object
         * }
         */
        if (value) {
          if (isGraphElement(value)) {
            return this.revertGraphObject(key, value);
          } else if (isSingularElement(value) || isContainerElement(value)) {
            return this.revertNormalObject(key, value);
          } else if (isInitElement(value)) {
            return this.emptyObject(key);
          } else {
            // which should never happen
            console.error('Variable Element Type Not Match!');
            return undefined;
          }
        } else {
          return this.emptyObject(key);
        }
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
