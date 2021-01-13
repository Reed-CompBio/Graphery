<template>
  <q-card flat id="display-element-wrapper">
    <div v-if="isContainer" id="container-abbr">
      <q-btn
        outline
        dense
        :label="containerAbbr"
        @click="handleContainerClick"
      />
    </div>
    <div v-else id="singular-display">
      {{ displayObjectContent }}
    </div>
    <!--  TODO cursor type change   -->
  </q-card>
</template>

<script>
  import { _REPR_HEADER } from '@/components/framework/VariableListComponents/variableListConstants';

  export default {
    props: ['index', 'initObject'],
    computed: {
      displayObject() {
        return this.initObject;
      },
      displayObjectContent() {
        return this.displayObject[_REPR_HEADER];
      },
      isContainer() {
        return Array.isArray(this.displayObjectContent);
      },
    },
    data() {
      return {
        containerAbbr: '...',
      };
    },
    methods: {
      handleContainerClick() {
        this.$emit('pushVariableStack', this.index, this.displayObject);
      },
    },
  };
</script>

<style lang="sass" scoped>
  #display-element-wrapper
    margin: 4px 0
    & #singular-display
      text-wrap: normal
      border-radius: 0.4rem
      padding: .15rem .3rem
      border: 0.1rem solid #1D1D1D
</style>
