<!-- TODO use pop up edit? -->
<template>
  <div id="code-controller-wrapper" class="full-height row flex-center">
    <q-virtual-scroll
      class="full-height"
      :items="variableDisplayList"
      id="variable-list-scroll"
    >
      <template v-slot="{ item, index }">
        <q-card :key="index" class="q-my-lg q-py-sm q-px-md text-center">
          <div class="mock-h6">
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

  export default {
    data() {
      return {
        sliderPos: 1,
      };
    },
    computed: {
      ...mapState('tutorials', ['variableObj']),
      ...mapGetters('tutorials', ['variableObjEmpty']),
      variableDisplayList() {
        if (this.variableObjEmpty) {
          return [
            {
              label: 'Status',
              value: 'Empty',
            },
          ];
        }
        const variableList = [];
        console.log(this.variableObj);
        for (const [key, value] of Object.entries(this.variableObj)) {
          let variableValue;
          if (value) {
            if (typeof value === 'object') {
              variableValue = value['label'];
            } else {
              variableValue = value;
            }
          } else {
            variableValue = 'Empty';
          }
          variableList.push({
            label: key.split('#')[1],
            value: variableValue,
          });
        }
        return variableList;
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
