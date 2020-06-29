<!-- TODO use pop up edit? -->
<template>
  <div id="code-controller-wrapper" class="full-height">
    <div id="stepper-button-group" class="row flex-center"></div>
    <div id="controller-section" class="row">
      <div id="stepper-section" class="col-3">
        <div id="stepper-slider" class="flex-center">
          <div class="q-mx-md"></div>
        </div>
      </div>
      <div id="variable-section" class="col-9">
        <q-virtual-scroll class="flex-center" :items="variableDisplayList">
          <template v-slot="{ item, index }">
            <q-card style="width: 70%" :key="index"
              >#{{ index }} - {{ item.label }} - {{ item.value }}</q-card
            >
          </template>
        </q-virtual-scroll>
      </div>
    </div>
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
