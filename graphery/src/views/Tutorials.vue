<template>
  <CollectionPage
    :title="$t('nav.Tutorials')"
    api="tutorials-api-path"
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
