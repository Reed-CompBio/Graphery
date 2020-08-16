<template>
  <CollectionPage
    :title="$t('nav.Graphs')"
    ref="collection"
    :query="query"
    :variables="{ translation: $i18n.locale }"
    :mappingFunction="
      (data) => {
        const input = data.allGraphInfo;
        return input.map((ele) => {
          return {
            url: `/graph/${ele.url}`,
            categories: ele.categories.map((obj) => obj.category),
            isAnchorPublished: ele.isPublished,
            title: ele.content.title,
            authors: ele.authors.map((obj) => obj.username),
            modifiedTime: ele.modifiedTime,
            abstract: ele.content.abstract,
            isTransPublished: ele.content.isPublished,
          };
        });
      }
    "
    moreButtonText="Play With it"
    :notClickableWhenNoContent="false"
  ></CollectionPage>
</template>

<script>
  import { allGraphAbstractInfoQuery } from '@/services/queries';
  export default {
    components: {
      CollectionPage: () =>
        import('@/components/CollectionEntry/CollectionPage.vue'),
    },
    data() {
      return {
        query: allGraphAbstractInfoQuery,
      };
    },
  };
</script>
