<template>
  <CollectionPage
    :title="$t('nav.Tutorials')"
    ref="collection"
    :query="query"
    :variables="{ translation: $i18n.locale }"
    :mappingFunction="
      (data) => {
        const input = data.allTutorialInfo;
        return input.map((ele) => {
          return {
            url: `/tutorial/${ele.url}`,
            categories: ele.categories.map((obj) => obj.category),
            isAnchorPublished: ele.isPublished,
            title: ele.content.title,
            authors: ele.content.authors.map((obj) => obj.username),
            modifiedTime: ele.content.modifiedTime,
            abstract: ele.content.abstract,
            isTransPublished: ele.content.isPublished,
          };
        });
      }
    "
    moreButtonText="Read More"
    :notClickableWhenNoContent="true"
  ></CollectionPage>
</template>

<script>
  import { allTutorialAbstractInfoQuery } from '@/services/queries';

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
