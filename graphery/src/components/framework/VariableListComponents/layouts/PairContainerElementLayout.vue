<template>
  <div id="pair-layout-wrapper">
    <div id="pair-layout-style-wrapper" class="fit">
      <div id="pair-container">
        <div id="empty-row-container" v-if="isEmpty">
          <VariableDisplayElementWrapper
            :init-object="{ repr: 'Empty Mapping' }"
          />
        </div>
        <div id="content-row-container" class="col" v-else>
          <div
            id="row-container"
            :key="index"
            class="row content-center"
            v-for="(pairElement, index) in pairElementArray"
          >
            <div id="row-key-container" class="col q-mx-xs center-item">
              <VariableDisplayElementWrapper
                v-on="$listeners"
                :init-object="pairElement['key']"
                :index="`[${index}]`"
              />
            </div>
            <div id="row-separator-wrapper">
              <div id="row-separator">
                <div>
                  :
                </div>
              </div>
            </div>
            <div id="row-value-container" class="col q-mx-xs fit">
              <VariableDisplayElementWrapper
                v-on="$listeners"
                :init-object="pairElement['value']"
                :index="`[${pairElement['key']['repr']}]`"
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
  #row-separator-wrapper
    display: flex
    justify-content: center
    align-items: center

  #row-separator
    padding: .15rem .3rem
    margin: auto
    background-color: rgba(130, 130, 130, 0.75)
    border-radius: 0.4rem
    max-width: 1rem
    display: block
    font-weight: bolder
    font-size: 1rem
</style>
