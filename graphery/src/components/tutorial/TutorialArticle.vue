<template>
  <v-col class="fill-height " cols="6">
    <!-- do not make v-rol the root element-->
    <!-- make a new loading indicator -->
    <PostLoadIndicator number="7"></PostLoadIndicator>
    <v-card id="article-card" max-height="100%" class="article-card">
      <v-card-text v-html="content"> </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';
  import PostLoadIndicator from './PostLoadIndicator';

  export default {
    components: {
      PostLoadIndicator,
    },
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
