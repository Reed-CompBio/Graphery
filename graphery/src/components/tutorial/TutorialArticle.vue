<template>
  <!-- make a new loading indicator -->
  <div>
    <!-- add a overlay -->
    <v-content
      v-show="!articleEmpty"
      id="article-card"
      style="max-height: 100%"
    >
      <v-card-text v-html="content" style="max-height: 90%; overflow: auto;">
      </v-card-text>
    </v-content>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex';
  import PostLoadIndicator from './PostLoadIndicator';

  export default {
    components: {},
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
      this.loadTutorial();
    },
  };
</script>
