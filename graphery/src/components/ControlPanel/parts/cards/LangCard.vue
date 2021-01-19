<template>
  <InfoCard>
    <template v-slot:title>
      Language
    </template>
    <div class="text-center">
      {{ displayedLang }}
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from './InfoCard.vue';
  import { langList } from '@/services/params';
  export default {
    props: ['lang'],
    components: {
      InfoCard,
    },
    computed: {
      displayedLang() {
        if (this.lang && !langList.includes(this.lang)) {
          return `Language "${this.lang}" NOT supported!`;
        }
        return this.lang;
      },
    },
  };
</script>
