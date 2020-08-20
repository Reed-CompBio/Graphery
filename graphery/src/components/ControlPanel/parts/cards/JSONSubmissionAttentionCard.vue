<template>
  <InfoCard>
    <template v-slot:title>
      <span class="text-bold text-italic">IMPORTANT</span>
    </template>
    <div class="text-bold">
      Please submit your code first!
    </div>
  </InfoCard>
</template>

<script>
  export default {
    components: {
      InfoCard: () => import('./InfoCard.vue'),
    },
  };
</script>
