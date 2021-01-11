<template>
  <q-card flat id="display-element-wrapper" @click="handleClick">
    <div v-if="isContainer" id="container-abbr">
      ...
    </div>
    <div v-else id="singular-display" style="text-wrap: normal">
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
    methods: {
      handleClick() {
        if (this.isContainer) {
          this.$emit('forward', this.index);
        }
      },
    },
  };
</script>

<style lang="sass" scoped>
  #display-element-wrapper
</style>
