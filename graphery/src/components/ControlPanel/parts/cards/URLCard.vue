<template>
  <InfoCard>
    <template v-slot:title>
      URL
    </template>
    <div class="text-center">
      <q-btn
        flat
        type="a"
        style="text-transform: none;"
        :label="displayedURL"
        :href="routePath"
        target="_blank"
      />
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from './InfoCard.vue';
  export default {
    props: {
      url: {
        type: String,
      },
      routePath: {
        type: String,
      },
    },
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
