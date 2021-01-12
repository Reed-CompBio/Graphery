<template>
  <div id="pair-layout-wrapper">
    <div id="pair-layout-style-wrapper" class="fit">
      <div id="pair-container" class="column ">
        <div id="empty-row-container" v-if="isEmpty">
          <VariableDisplayElementWrapper
            :init-object="{ repr: 'Empty Mapping' }"
          />
        </div>
        <div id="content-row-container" v-else>
          <div
            id="row-container"
            :key="index"
            class="row content-center flex-center"
            v-for="(pairElement, index) in pairElementArray"
          >
            <div id="row-key-container" class="col-5 q-mx-xs">
              <VariableDisplayElementWrapper
                :init-object="pairElement['key']"
                :index="index"
              />
            </div>
            <div id="row-separator">
              :
            </div>
            <div id="row-value-container" class="col-5 q-mx-xs">
              <VariableDisplayElementWrapper
                :init-object="pairElement['value']"
                :index="index"
              />
            </div>
          </div>
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
      pairElementArray() {
        return this.initElement[_REPR_HEADER];
      },
      isEmpty() {
        return this.initElement[_REPR_HEADER].length === 0;
      },
    },
  };
</script>

<style lang="sass" scoped>
  #row-separator
    padding: .2em .4em
    margin: 0
    background-color: #828282
    border-radius: 6px
</style>
