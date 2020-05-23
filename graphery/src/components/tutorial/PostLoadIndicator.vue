<template>
  <div>
    <v-skeleton-loader
      class="px-2"
      type="article"
      v-for="i in index"
      :key="i"
    ></v-skeleton-loader>
  </div>
</template>

<script>
  export default {
    props: ['number'],
    computed: {
      index() {
        return Array.from({ length: this.number }, (v, i) => i);
      },
    },
  };
</script>
