<!-- TODO use pop up edit? -->
<template>
  <div id="code-controller-wrapper" class="full-height row flex-center">
    <q-virtual-scroll
      class="full-height"
      :items="variableDisplayList"
      id="variable-list-scroll"
    >
      <!-- make cards wrap when the width is enough -->
      <template v-slot="{ item, index }">
        <q-card :key="index" class="q-my-md q-py-sm q-px-md text-center">
          <div class="mock-h6" :style="`background-color: ${item.color}`">
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

        for (const [key, value] of Object.entries(this.variableObj)) {
          let variableValue;
          let variableColor;
          if (value) {
            if (typeof value === 'object') {
              variableValue = value['label'];
              variableColor = value['color'];
            } else {
              variableValue = value;
            }
          } else {
            variableValue = 'Empty';
          }
          variableList.push({
            // TODO temporary work round
            label: key.split('#')[1],
            color: variableColor,
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
