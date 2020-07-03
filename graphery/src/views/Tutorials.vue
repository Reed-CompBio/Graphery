<template>
  <CollectionPage
    :title="$t('nav.Tutorials')"
    ref="collection"
  ></CollectionPage>
</template>

<script>
  import { allTutorialAbstractInfoQuery } from '../services/queries';
  import { apiCaller } from '../services/apis';
  import CollectionPage from '@/components/CollectionEntry/CollectionPage.vue';

  export default {
    components: {
      CollectionPage: CollectionPage,
    },
    data() {
      return {
        query: allTutorialAbstractInfoQuery,
      };
    },
    methods: {
      mapToInterface(input) {
        return input.map((ele) => {
          return {
            url: ele.url,
            categories: ele.categories,
            isAnchorPublished: ele.isPublished,
            title: ele.content.title,
            authors: ele.content.authors,
            modifiedTime: ele.content.modifiedTime,
            abstract: ele.content.abstract,
            isTransPublished: ele.content.isPublished,
          };
        });
      },
      getInfoList() {
        console.debug('api query: ', this.query);

        const collectionPage = this.$refs.collection;

        collectionPage.toggleLoading();

        apiCaller(this.query, this.variables)
          .then(([data, errors]) => {
            if (errors !== undefined && !data) {
              console.error(errors);
            }
            collectionPage.loadInfo(this.mapToInterface(data.allTutorialInfo));

            collectionPage.finishLoading();
          })
          .catch((err) => {
            // TODO show pop up here
            console.error(err);
          });
      },
    },
    mounted() {
      this.getInfoList();
    },
  };
</script>
