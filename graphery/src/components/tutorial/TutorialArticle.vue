<template>
  <!-- make a new loading indicator -->
  <div class="full-height">
    <!-- add a overlay -->

    <q-scroll-area ref="tc" v-show="!articleEmpty" class="full-height q-px-lg">
      <div class="q-mt-xl">
        <div id="tutorial-title" class="text-h2">{{ title }}</div>
        <div id="tutorial-info" class="q-mb-lg">
          <q-breadcrumbs>
            <q-breadcrumbs-el>
              <span>Author: </span>
              <span v-for="author in authors" :key="author">
                {{ author }}
              </span>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el>
              <span> Category: </span>
              <span v-for="category in categories" :key="category">
                {{ category }}
              </span>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el>
              {{ articleTime }}
            </q-breadcrumbs-el>
            <q-breadcrumbs-el>
              <q-btn flat rounded dense @click="share">
                <q-icon name="mdi-share-variant"></q-icon>
              </q-btn>
            </q-breadcrumbs-el>
          </q-breadcrumbs>
        </div>
      </div>
      <div id="tutorial-content" v-html="content"></div>
    </q-scroll-area>
    <q-page-sticky position="bottom-right" :offset="[30, 30]">
      <q-btn round color="primary" icon="mdi-menu-up" @click="scrollToTop" />
    </q-page-sticky>
    <q-inner-loading
      :showing="articleEmpty"
      transition-show="fade"
      transition-hide="fade"
    >
      <q-spinner-radio size="64px" color="primary"></q-spinner-radio>
    </q-inner-loading>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex';

  export default {
    computed: {
      ...mapState('tutorials', ['article']),
      ...mapGetters('tutorials', [
        'articleEmpty',
        'title',
        'content',
        'authors',
        'categories',
        'articleTime',
      ]),
    },
    methods: {
      ...mapActions('tutorials', ['loadTutorial']),
      share() {
        // TODO copy to clipboard
      },
      scrollToTop() {
        this.$refs.tc.setScrollPosition(0, 500);
      },
    },
    mounted() {
      // this.loadTutorial();
      // when should I load the text hmmmmm
    },
  };
</script>
