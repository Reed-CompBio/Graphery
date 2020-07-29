<template>
  <InfoCard>
    <template v-slot:title>
      Language
    </template>
    <div class="text-center">
      {{ lang }}
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from '../parts/InfoCard.vue';
  export default {
    props: ['lang'],
    components: {
      InfoCard,
    },
  };
</script>
