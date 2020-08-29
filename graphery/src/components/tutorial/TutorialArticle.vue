<template>
  <div id="articleWrapper" style="overflow-y: auto;">
    <div
      id="tutorial-container"
      ref="tc"
      v-show="!articleEmpty"
      class="q-px-lg q-pb-xl"
    >
      <div id="tutorial-wrapper" class="q-mt-xl">
        <div id="tutorial-title" class="text-h3 q-mb-lg">
          {{ title }}
        </div>
        <div id="tutorial-info" class="q-mb-lg">
          <div>
            <q-chip clickable v-if="!isAnchorPublished" icon="mdi-book-lock">
              Tutorial Not Published
            </q-chip>
            <q-chip clickable v-if="!isTransPublished" icon="mdi-book-lock">
              Translation Not Published
            </q-chip>
          </div>
          <q-chip icon="trending_up">
            {{ rankText }}
          </q-chip>
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
          <q-chip
            clickable
            v-for="category in categories"
            :key="category"
            icon="category"
            @click="$emit('category-filter', category)"
          >
            {{ category }}
          </q-chip>
          <q-chip icon="mdi-calendar-month">
            {{ toLocalDateString($i18n.locale, articleModTime) }}</q-chip
          >
          <q-btn flat rounded dense @click="share">
            <SwitchTooltip :text="$t('tooltips.Share')"></SwitchTooltip>
            <q-icon name="mdi-share-variant"></q-icon>
          </q-btn>
        </div>

        <!-- actual contents goes into here -->
        <div id="tutorial-content">
          <MarkdownSection
            :input-html="htmlContent"
            :breakpoint-react="true"
            :highlight="true"
            @breakpointClicked="
              (position) => {
                $emit('breakpointClicked', position);
              }
            "
          ></MarkdownSection>
        </div>

        <LicenseCard></LicenseCard>
      </div>
    </div>

    <q-inner-loading
      :showing="articleEmpty"
      transition-show="fade"
      transition-hide="fade"
    >
      <q-spinner-pie size="64px" color="primary"></q-spinner-pie>
    </q-inner-loading>

    <q-page-sticky position="bottom-right" :offset="[30, 30]">
      <transition
        appear
        enter-active-class="animated zoomIn"
        leave-active-class="animated zoomOut"
      >
        <!-- TODO use quasar native utils to get percentage and replace the scroll func I wrote  -->
        <q-circular-progress
          size="42px"
          :value="1"
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
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';
  import {
    toLocalDateString,
    saveTextToClipboard,
    successDialog,
  } from '@/services/helpers';
  import MarkdownSection from '@/components/framework/md/MarkdownSection';

  export default {
    metaInfo() {
      const articleTitle = this.headerTitle;
      return { title: articleTitle };
    },
    components: {
      MarkdownSection,
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
      LicenseCard: () => import('@/components/framework/LicenseCard.vue'),
    },
    data() {
      return {
        // articleViewPercentage: 0,
      };
    },
    computed: {
      ...mapGetters('tutorials', [
        'articleEmpty',
        'title',
        'htmlContent',
        'authors',
        'categories',
        'articleModTime',
        'isAnchorPublished',
        'isTransPublished',
        'rankText',
      ]),
      headerTitle() {
        return this.title ? this.title : this.$t('metaInfo.Tutorial');
      },
    },
    methods: {
      toLocalDateString,
      share() {
        saveTextToClipboard(window.location.href);
        // TODO use uniform notify
        successDialog({ message: 'The URL of this tutorial is copied.' });
      },
      scrollToTop() {
        document.getElementById('articleWrapper').scrollTo({
          top: 0,
          behavior: 'smooth',
        });
      },
    },
  };
</script>

<style lang="sass">
  @import '~@quasar/extras/animate/zoomIn.css'
  @import '~@quasar/extras/animate/zoomOut.css'

  #scroll-up-icon:hover
    cursor: pointer
  #tutorial-content h2
    font-size: 28px
    margin: 8px 0
    font-style: oblique
</style>
