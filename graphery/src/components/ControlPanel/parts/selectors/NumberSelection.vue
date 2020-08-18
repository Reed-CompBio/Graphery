<template>
  <q-select
    :options="numbers"
    v-model="modelNumber"
    :label="label"
    :option-label="formatter"
  />
</template>

<script>
  export default {
    props: {
      start: {
        type: Number,
        default: 0,
      },
      end: {
        type: Number,
        default: 9,
      },
      label: {
        type: String,
        default: '',
      },
      currentNumber: {
        type: Number,
        default: 0,
      },
      formatter: {
        type: Function,
        default: null,
      },
    },
    model: {
      prop: 'currentNumber',
      event: 'updateNumber',
    },
    computed: {
      modelNumber: {
        set(d) {
          this.$emit('updateNumber', d);
        },
        get() {
          return this.currentNumber;
        },
      },
      numbers() {
        const list = [];
        for (let i = this.start; i <= this.end; i++) {
          list.push(i);
        }
        return list;
      },
    },
  };
</script>
