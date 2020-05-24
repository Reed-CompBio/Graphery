<template>
  <!-- make a new loading indicator -->
  <div>
    <!-- add a overlay -->
    <q-page-container
      v-show="!articleEmpty"
      id="article-container"
      style="max-height: 100%"
    >
      <div class="text-h1">{{ title }}</div>
      <div>
        <q-breadcrumbs>
          <q-breadcrumbs-el> By {{ author }} </q-breadcrumbs-el>
          <q-breadcrumbs-el>
            {{ category }}
          </q-breadcrumbs-el>
          <q-breadcrumbs-el>
            {{ articleTime }}
          </q-breadcrumbs-el>
          <q-breadcrumbs-el>
            <q-icon name="mdi-share-variant"></q-icon>
          </q-breadcrumbs-el>
        </q-breadcrumbs>
      </div>
      <q-scroll-area v-html="content" style="max-height: 90%;"> </q-scroll-area>
    </q-page-container>
    <q-page-sticky position="bottom-right" :offset="[10, 10]">
      <q-btn round color="primary" icon="arrow_forward" class="rotate-45" />
    </q-page-sticky>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex';
  import PostLoadIndicator from './PostLoadIndicator';

  export default {
    components: {},
    computed: {
      ...mapState('tutorials', ['article']),
      ...mapGetters('tutorials', [
        'articleEmpty',
        'title',
        'content',
        'author',
        'category',
        'articleTime',
      ]),
    },
    methods: {
      ...mapActions('tutorials', ['loadTutorial']),
      share() {
        // TODO copy to clipboard
      },
    },
    mounted() {
      // this.loadTutorial();
      // when should I load the text hmmmmm
      this.loadTutorial();
    },
  };
</script>
