<template>
  <CollectionPage :title="$t('nav.Tutorials')" :query="query"></CollectionPage>
</template>

<script>
  import { allTutorialAbstractInfoQuery } from '../services/queries';
  export default {
    components: {
      CollectionPage: () =>
        import('@/components/CollectionEntry/CollectionPage.vue'),
    },
    data() {
      return {
        query: allTutorialAbstractInfoQuery,
      };
    },
  };
</script>
