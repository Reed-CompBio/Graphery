<template>
  <div id="articleWrapper">
    <div
      ref="tc"
      v-show="!articleEmpty"
      class="full-height q-px-lg"
      style="overflow-y: auto; overflow-x: hidden;"
    >
      <div class="q-mt-xl">
        <div id="tutorial-title" class="text-h2">{{ title }}</div>
        <div id="tutorial-info" class="q-mb-lg">
          <q-breadcrumbs>
            <q-breadcrumbs-el v-if="authors">
              <q-chip
                clickable
                v-for="author in authors"
                :key="author"
                icon="mdi-card-account-details"
                @click="$emit('author-filter', author)"
              >
                <!-- may be I don't need the author filter -->
                {{ author }}
              </q-chip>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el v-if="categories">
              <q-chip
                clickable
                v-for="category in categories"
                :key="category"
                icon="category"
                @click="$emit('category-filter', category)"
              >
                {{ category }}
              </q-chip>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el v-if="articleTime">
              <q-chip icon="mdi-calendar-month"> {{ articleTime }}</q-chip>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el>
              <q-btn flat rounded dense @click="share">
                <SwitchTooltip :text="$t('tooltips.Share')"></SwitchTooltip>
                <q-icon name="mdi-share-variant"></q-icon>
              </q-btn>
            </q-breadcrumbs-el>
          </q-breadcrumbs>
        </div>
      </div>

      <!-- actual contents goes into here -->
      <div id="tutorial-content" v-html="content"></div>

      <LicenseCard></LicenseCard>

      <div class="q-mb-xl"></div>
    </div>
    <!-- add a protocol info section -->

    <q-page-sticky position="bottom-right" :offset="[30, 30]">
      <transition
        appear
        enter-active-class="animated zoomIn"
        leave-active-class="animated zoomOut"
      >
        <!-- TODO fix this? -->
        <q-circular-progress
          v-show="articleViewPercentage !== 0"
          size="42px"
          :value="articleViewPercentage"
          :max="1"
          color="primary"
          :thickness="0.1"
          center-color="primary"
          track-color="white"
          show-value
          @click="scrollToTop"
        >
          <q-icon
            id="scroll-up-icon"
            name="mdi-menu-up"
            color="white"
            size="26px"
          />
        </q-circular-progress>
      </transition>
    </q-page-sticky>
    <q-inner-loading
      :showing="articleEmpty"
      transition-show="fade"
      transition-hide="fade"
    >
      <q-spinner-pie size="64px" color="primary"></q-spinner-pie>
    </q-inner-loading>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex';

  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
      LicenseCard: () => import('@/components/framework/LicenseCard.vue'),
    },
    data() {
      return {
        articleViewPercentage: 0,
      };
    },
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

      updatePosPercentage(info) {
        console.log(info);
      },
      scrollToTop() {
        document.getElementById('articleWrapper').scrollTo({
          top: 0,
          left: 0,
          behavior: 'smooth',
        });
      },
    },
    mounted() {
      // this.loadTutorial();
      // TODO when you access the page from tutorials or graphs, the article is not shown.
      //    SINCE there is not real api call!!!
      // TODO when should I load the text hmmmmm
    },
  };
</script>

<style lang="sass">
  @import '~@quasar/extras/animate/zoomIn.css'
  @import '~@quasar/extras/animate/zoomOut.css'

  #scroll-up-icon:hover
    cursor: pointer
</style>
