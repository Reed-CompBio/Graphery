<template>
  <CollectionPage title="Tutorials" api="tutorials-api-path"></CollectionPage>
</template>

<script>
  export default {
    components: {
      CollectionPage: () => import('@/components/framework/CollectionPage.vue'),
    },
  };
</script>
