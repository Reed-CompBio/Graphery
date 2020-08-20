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
  import { mapGetters, mapState } from 'vuex';
  import {
    EMPTY_VARIABLE_ELEMENT_DISPLAY,
    GRAPH_ELEMENT_TYPE,
    NORMAL_VARIABLE_TYPE,
    VARIABLE_EMPTY_CONTENT_NOTATION,
  } from '@/components/framework/GraphEditorControls/parameters';

  export default {
    props: ['variableObject'],
    data() {
      return {
        sliderPos: 1,
      };
    },
    computed: {
      ...mapState('tutorials', ['variableObj']),
      ...mapGetters('tutorials', ['variableObjEmpty']),
      ...mapGetters('variables', ['getCurrentVariables']),
      currentVariables() {
        return this.getCurrentVariables;
      },
      currentVariablesEmpty() {
        return this.currentVariables === VARIABLE_EMPTY_CONTENT_NOTATION;
      },
      variableDisplayList() {
        if (this.currentVariablesEmpty) {
          return [
            {
              label: 'Status',
              value: '<Empty>',
            },
          ];
        }
        const variableList = [];

        for (const [key, value] of Object.entries(this.currentVariables)) {
          variableList.push(this.processVariableElement(key, value));
        }
        return variableList;
      },
    },
    methods: {
      revertNameCombo(nameCombo) {
        return nameCombo.split('#')[1];
      },
      revertGraphObject(nameCombo, element) {
        return {
          // TODO temporary work round figure out how to style it
          label: this.revertNameCombo(nameCombo),
          color: element['color'],
          value: element['repr'],
        };
      },
      revertNormalObject(nameCombo, element) {
        return {
          label: this.revertNameCombo(nameCombo),
          color: undefined,
          value: element['repr'],
        };
      },
      emptyObject(nameCombo) {
        return {
          label: this.revertNameCombo(nameCombo),
          color: undefined,
          value: EMPTY_VARIABLE_ELEMENT_DISPLAY,
        };
      },
      processVariableElement(key, value) {
        if (value) {
          if (value.type === GRAPH_ELEMENT_TYPE) {
            return this.revertGraphObject(key, value);
          } else if (value.type === NORMAL_VARIABLE_TYPE) {
            return this.revertNormalObject(key, value);
          } else {
            // which should never happen
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
