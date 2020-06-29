<!-- TODO use pop up edit? -->
<template>
  <div id="code-controller-wrapper" class="full-height row flex-center">
    <q-virtual-scroll
      class=""
      :items="variableDisplayList"
      id="variable-list-scroll"
    >
      <template v-slot="{ item, index }">
        <q-card :key="index" class="q-py-sm q-px-md text-center">
          <h6 style="margin: 0 0">
            {{ item.label }}
          </h6>
          {{ item.value }}
        </q-card>
      </template>
    </q-virtual-scroll>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';

  export default {
    data() {
      return {
        sliderPos: 1,
      };
    },
    computed: {
      ...mapGetters('tutorials', ['resultJsonEmpty', 'variableObjEmpty']),
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
          if (typeof value === 'object') {
            variableValue = value['id'];
          } else {
            variableValue = value;
          }
          variableList.push({
            label: key.split('#').join('.'),
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
</style>
