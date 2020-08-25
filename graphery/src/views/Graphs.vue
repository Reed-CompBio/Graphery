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
            url: `/graph/${$i18n.locale}/${ele.url}`,
            categories: ele.categories,
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
    metaInfo() {
      const titleText = this.$t('nav.Graphs');
      return { title: titleText };
    },
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
