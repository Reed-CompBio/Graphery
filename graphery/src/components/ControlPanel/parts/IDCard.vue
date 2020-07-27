<template>
  <InfoCard>
    <template v-slot:title>
      ID
    </template>
    <div class="text-center">
      {{ displayedId }}
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from '../parts/InfoCard.vue';
  import { newModelUUID } from '../../../services/params';
  export default {
    props: ['id'],
    components: {
      InfoCard,
    },
    computed: {
      displayedId() {
        return this.id === newModelUUID ? 'Pending' : this.id;
      },
    },
  };
</script>
