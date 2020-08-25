<template>
  <span v-if="hasRank">{{ rankText }}</span>
  <span v-else></span>
</template>

<script>
  import { rankToText } from '@/services/helpers';

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
      rankText() {
        return rankToText(this.rank);
      },
    },
  };
</script>
