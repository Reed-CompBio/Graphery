<template>
  <InfoCard>
    <template v-slot:title>
      {{ title }}
    </template>
    <div class="text-center">
      {{ displayedId }}
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from './InfoCard.vue';
  import { newModelUUID } from '@/services/params';
  export default {
    props: {
      id: {
        type: String,
      },
      title: {
        type: String,
        default: 'ID',
      },
    },
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
