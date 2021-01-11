<template>
  <div id="linear-layout-wrapper">
    <div id="linear-layout-style-wrapper">
      <div id="linear-list-container">
        <VariableDisplayElementWrapper
          :init-object="arrayElement"
          :index="index"
          :key="index"
          v-for="(arrayElement, index) in arrayElements"
        />
      </div>
    </div>
  </div>
</template>

<script>
  import VariableDisplayElementWrapper from '@/components/framework/VariableListComponents/VariableDisplayElementWrapper';
  import { _REPR_HEADER } from '@/components/framework/VariableListComponents/variableListConstants';
  export default {
    components: { VariableDisplayElementWrapper },
    props: {
      initElement: {
        type: Array,
      },
    },
    computed: {
      arrayElements() {
        return this.initElement[_REPR_HEADER];
      },
    },
  };
</script>

<style lang="sass" scoped></style>
