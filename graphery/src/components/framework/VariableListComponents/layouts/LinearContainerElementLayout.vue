<template>
  <div id="linear-layout-wrapper">
    <div id="linear-layout-style-wrapper">
      <div id="empty-row-container" v-if="isEmpty">
        <VariableDisplayElementWrapper
          :init-object="{ repr: 'Empty Sequence' }"
        />
      </div>
      <div id="content-row-container" v-else>
        <div id="linear-list-container">
          <VariableDisplayElementWrapper
            :init-object="arrayElement"
            :index="`[${index}]`"
            :key="index"
            v-on="$listeners"
            v-for="(arrayElement, index) in arrayElements"
          />
        </div>
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
        type: Object,
      },
    },
    computed: {
      arrayElements() {
        return this.initElement[_REPR_HEADER];
      },
      isEmpty() {
        return this.arrayElements.length === 0;
      },
    },
  };
</script>

<style lang="sass" scoped></style>
