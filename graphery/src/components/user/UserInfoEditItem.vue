<template>
  <q-item>
    <q-item-section>
      <q-input
        v-model="model"
        :type="type"
        outlined
        :name="name"
        @input="emitInput"
        :debounce="debounce"
        :rules="rules"
        :lazy-rules="lazyRules"
        :hint="hint"
        :label="label"
      >
        <template v-slot:append>
          <slot name="append" />
        </template>
      </q-input>
    </q-item-section>
  </q-item>
</template>

<script>
  export default {
    props: {
      type: {
        type: String,
        default: 'password',
      },
      name: { type: String, default: 'default' },
      initValue: { type: String, default: '' },
      debounce: { type: Number, default: 0 },
      rules: { type: Array, default: undefined },
      lazyRules: { type: Boolean, default: true },
      hint: { type: String, default: '' },
      label: { type: String, default: '' },
    },
    model: {
      prop: 'model',
      event: 'input',
    },
    data() {
      return {
        model_: this.initValue,
      };
    },
    computed: {
      model: {
        set(d) {
          this.model_ = d;
        },
        get() {
          return this.model_;
        },
      },
    },
    methods: {
      emitInput(value) {
        this.$emit('input', value);
      },
    },
  };
</script>
