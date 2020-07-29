<template>
  <InfoCard>
    <template v-slot:title>
      URL
    </template>
    <div class="text-center">
      {{ displayedURL }}
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from '../parts/InfoCard.vue';
  export default {
    props: ['url'],
    components: {
      InfoCard,
    },
    computed: {
      displayedURL() {
        return this.url;
      },
    },
  };
</script>
