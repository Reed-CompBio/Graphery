<template>
  <div id="singular-layout-wrapper">
    <div id="singular-layout-style-wrapper">
      <VariableDisplayElementWrapper :init-object="element" />
    </div>
  </div>
</template>

<script>
  import VariableDisplayElementWrapper from '@/components/framework/VariableListComponents/VariableDisplayElementWrapper';
  import { isInitElement } from '@/components/framework/GraphEditorControls/ElementsUtils';
  import {
    _EMPTY_TYPE_STRING,
    _REPR_HEADER,
  } from '@/components/framework/VariableListComponents/variableListConstants';
  export default {
    components: { VariableDisplayElementWrapper },
    props: {
      initElement: {
        type: Object,
      },
    },
    computed: {
      element() {
        if (isInitElement(this.initElement)) {
          return {
            ...this.initElement,
            [_REPR_HEADER]: _EMPTY_TYPE_STRING,
          };
        } else {
          return this.initElement;
        }
      },
    },
  };
</script>

<style lang="sass" scoped></style>
