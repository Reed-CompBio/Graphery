<template>
  <div id="pair-layout-wrapper">
    <div id="pair-layout-style-wrapper" class="fit">
      <div id="pair-container" class="column ">
        <div id="empty-row-container" v-if="isEmpty">
          <VariableDisplayElementWrapper
            :init-object="{ repr: 'Empty Mapping' }"
          />
        </div>
        <div id="content-row-container" class="col" v-else>
          <div
            id="row-container"
            :key="index"
            class="row justify-center content-center"
            v-for="(pairElement, index) in pairElementArray"
          >
            <div id="row-key-container" class="col-5 q-mx-xs">
              <VariableDisplayElementWrapper
                v-on="$listeners"
                :init-object="pairElement['key']"
                :index="index"
              />
            </div>
            <div
              id="row-separator-wrapper"
              class="col justify-center flex-center"
            >
              <div
                id="row-separator"
                style="max-width: 15px; display: inline-block;"
              >
                :
              </div>
            </div>
            <div id="row-value-container" class="col-5 q-mx-xs">
              <VariableDisplayElementWrapper
                v-on="$listeners"
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
        return this.pairElementArray.length === 0;
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
