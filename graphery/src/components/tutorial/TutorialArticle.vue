<template>
  <!-- make a new loading indicator -->
  <div style="max-height: 100%">
    <!-- add a overlay -->

    <q-scroll-area ref="tc" v-show="!articleEmpty">
      <div id="tutorial-title" class="text-h2">{{ title }}</div>
      <div id="tutorial-info">
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
      <div id="tutorial-content" v-html="content"></div>
    </q-scroll-area>
    <q-page-sticky position="bottom-right" :offset="[10, 10]">
      <q-btn round color="primary" icon="mdi-menu-up" @click="scrollToTop" />
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
      scrollToTop() {
        this.$ref.tc.setScrollPosition(0, 300);
      },
    },
    mounted() {
      // this.loadTutorial();
      // when should I load the text hmmmmm
      this.loadTutorial();
    },
  };
</script>
