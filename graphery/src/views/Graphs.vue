<template>
  <CollectionPage :title="$t('nav.Graphs')" ref="collection"></CollectionPage>
</template>

<script>
  import CollectionPage from '@/components/CollectionEntry/CollectionPage.vue';

  export default {
    components: {
      CollectionPage: CollectionPage,
    },
    mounted() {
      //TODO show pop up, coming soon
    },
  };
</script>
