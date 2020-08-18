<template>
  <span v-if="hasRank">{{ rank.level }}-{{ rank.section }}</span>
  <span v-else></span>
</template>

<script>
  export default {
    props: {
      rank: {
        type: Object,
        default: null,
      },
    },
    computed: {
      hasRank() {
        return this.rank !== null;
      },
    },
  };
</script>
