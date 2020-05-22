<template>
  <v-col class="fill-height article-col" cols="6">
    <!-- do not make v-rol the root element-->
    <v-skeleton-loader type="article" v-if="articleEmpty"></v-skeleton-loader>
    <v-card id="article-card" v-else class="article-card">
      <v-card-text v-html="content"> </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';

  export default {
    computed: {
      ...mapState('tutorials', ['article']),
      ...mapGetters('tutorials', ['articleEmpty']),
      title() {
        return this.article ? this.article.title : null;
      },
      content() {
        return this.article ? this.article.content : null;
      },
      value() {
        return false;
      },
    },
  };
</script>

<!-- style does not work -->
<style scoped>
  .article-col {
    display: flex;
  }

  .article-card {
    max-height: 100%;
    max-width: 100%;
  }

  .article-card > .article {
    flex: 1 1 auto;
  }

  .article-card > .v-card__text {
    backface-visibility: hidden;
    overflow-y: auto;
    flex: 1 1 auto;
  }
</style>
