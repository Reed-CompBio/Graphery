<template>
  <q-card flat id="display-element-wrapper">
    <div v-if="showAbbr" id="container-abbr">
      <q-btn outline dense :label="containerAbbr" @click="handleContainerClick">
        <SwitchTooltip :text="$t('variable.Expand Element')" />
      </q-btn>
    </div>
    <div v-else id="singular-display">
      {{ displayObjectContent }}
    </div>
    <!--  TODO cursor type change   -->
  </q-card>
</template>

<script>
  import {
    _REFERENCE_TYPE_STRING,
    _REPR_HEADER,
    _TYPE_HEADER,
  } from '@/components/framework/VariableListComponents/variableListConstants';
  import SwitchTooltip from '@/components/framework/SwitchTooltip';

  export default {
    components: { SwitchTooltip },
    props: ['index', 'initObject'],
    computed: {
      displayObject() {
        return this.initObject;
      },
      displayObjectContent() {
        return this.displayObject[_REPR_HEADER];
      },
      showAbbr() {
        return (
          Array.isArray(this.displayObjectContent) ||
          (this.initObject[_TYPE_HEADER] === _REFERENCE_TYPE_STRING &&
            this.displayObjectContent === null)
        );
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
    margin: 0.4rem 0
    & #singular-display
      text-wrap: normal
      border-radius: 0.4rem
      padding: .2rem .3rem
      border: 0.1rem solid #1D1D1D
</style>
