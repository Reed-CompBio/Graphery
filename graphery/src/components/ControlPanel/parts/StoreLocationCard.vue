<template>
  <InfoCard>
    <template v-slot:title>
      Using store location
    </template>
    {{ displayedLocation }}
  </InfoCard>
</template>

<script>
  export default {
    props: {
      location: {
        type: String,
      },
    },
    components: { InfoCard: () => import('../parts/InfoCard') },
    computed: {
      displayedLocation() {
        return this.location;
      },
    },
  };
</script>
