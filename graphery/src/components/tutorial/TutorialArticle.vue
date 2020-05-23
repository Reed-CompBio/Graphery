<template>
  <!-- make a new loading indicator -->
  <div>
    <PostLoadIndicator number="3" v-if="articleEmpty"></PostLoadIndicator>
    <v-content v-show="!articleEmpty" id="article-card" style="overflow: auto;">
      <v-card-text :v-html="content"> </v-card-text>
    </v-content>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex';
  import PostLoadIndicator from './PostLoadIndicator';

  export default {
    components: {
      PostLoadIndicator,
    },
    computed: {
      ...mapState('tutorials', ['article']),
      ...mapGetters('tutorials', ['articleEmpty', 'title', 'content']),
    },
    methods: {
      ...mapActions('tutorials', ['loadTutorial']),
    },
    mounted() {
      // this.loadTutorial();
      // when should I load the text hmmmmm
      // this.loadTutorial();
    },
  };
</script>
