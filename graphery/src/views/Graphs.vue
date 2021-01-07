<template>
  <CollectionPage
    :title="$t('nav.Graphs')"
    ref="collection"
    :query="query"
    :variables="{ translation: $i18n.locale, default: 'en-us' }"
    :mappingFunction="
      (data) => {
        const input = data.allGraphInfo;
        return input.map((ele) => {
          return {
            url: `/graph/${$i18n.locale}/${ele.url}`,
            categories: ele.categories,
            isAnchorPublished: ele.isPublished,
            title: ele.content.title,
            authors: ele.authors,
            modifiedTime: ele.modifiedTime,
            abstract: ele.content.abstract,
            isTransPublished: ele.content.isPublished,
          };
        });
      }
    "
    :moreButtonText="$t('collectionPage.PlayWithIt')"
    :notClickableWhenNoContent="false"
  ></CollectionPage>
</template>

<script>
  import { allGraphAbstractInfoQuery } from '@/services/queries';
  import CollectionPage from '@/components/CollectionEntry/CollectionPage';
  export default {
    metaInfo() {
      const titleText = this.$t('nav.Graphs');
      return { title: titleText };
    },
    components: {
      CollectionPage,
    },
    data() {
      return {
        query: allGraphAbstractInfoQuery,
      };
    },
  };
</script>
