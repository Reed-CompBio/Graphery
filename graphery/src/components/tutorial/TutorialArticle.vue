<template>
  <v-col>
    <!--do not make v-rol the root element-->
    <v-skeleton-loader type="article" v-if="value"></v-skeleton-loader>
    <v-card id="article" v-html="article" v-else></v-card>
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
