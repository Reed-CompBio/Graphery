<template>
  <CollectionPage title="Graphs" api="graphs-api-path"></CollectionPage>
</template>

<script>
  export default {
    components: {
      CollectionPage: () => import('@/components/framework/CollectionPage.vue'),
    },
    data() {
      return {
        searchText: '',
        searchLoading: false,
        filterSelections: [],
      };
    },
  };
</script>
