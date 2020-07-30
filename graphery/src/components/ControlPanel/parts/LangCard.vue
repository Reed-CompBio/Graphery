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
  import { langList } from '@/services/params';
  export default {
    props: ['lang'],
    components: {
      InfoCard,
    },
    computed: {
      displayedLang() {
        if (this.lang || !(this.lang in langList)) {
          return `Language "${this.lang}" NOT supported!`;
        }
        return this.lang;
      },
    },
  };
</script>
