<template>
  <CollectionPage
    :title="$t('nav.Graphs')"
    api="graphs-api-path"
  ></CollectionPage>
</template>

<script>
  export default {
    components: {
      CollectionPage: () =>
        import('@/components/CollectionEntry/CollectionPage.vue'),
    },
  };
</script>
