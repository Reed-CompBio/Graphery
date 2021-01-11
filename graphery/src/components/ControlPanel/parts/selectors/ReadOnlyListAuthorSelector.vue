<template>
  <q-select
    readonly
    use-chips
    multiple
    v-model="authors"
    map-options
    :option-label="(item) => `${item.firstName} ${item.lastName}`"
    option-value="id"
  ></q-select>
</template>

<script>
  export default {
    props: {
      initAuthors: {
        type: Object,
        default: undefined,
      },
    },
    computed: {
      authors() {
        return this.initAuthors ? this.initAuthors : [];
      },
    },
  };
</script>
