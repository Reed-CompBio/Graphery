<template>
  <div id="articleWrapper" style="overflow-y: hidden;">
    <q-scroll-area
      ref="tutorialScrollArea"
      @scroll="updateViewPercentage"
      class="fit"
    >
      <div
        id="tutorial-container"
        ref="tc"
        v-show="!articleEmpty"
        class="q-px-lg q-pb-xl full-height"
      >
        <div id="tutorial-wrapper" class="q-mt-xl full-height">
          <div id="tutorial-title-wrapper">
            <h1 id="tutorial-title" class="q-mb-lg">
              {{ title }}
            </h1>
          </div>
          <div id="tutorial-info-wrapper" class="q-mb-lg">
            <div id="publish-group">
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
              v-for="author in authors"
              :key="author.username"
              icon="mdi-card-account-details"
              @click="$emit('author-filter', author)"
            >
              <!-- may be I don't need the author filter -->
              {{ author.firstName }} {{ author.lastName }}
            </q-chip>
            <q-chip icon="mdi-calendar-month">
              {{ toLocalDateString($i18n.locale, articleModTime) }}</q-chip
            >
            <q-btn flat rounded dense @click="share">
              <SwitchTooltip :text="$t('tooltips.Share')"></SwitchTooltip>
              <q-icon name="mdi-share-variant"></q-icon>
            </q-btn>
            <div id="category-group">
              <q-chip
                clickable
                v-for="category in categories"
                :key="category"
                icon="category"
                @click="$emit('category-filter', category)"
              >
                {{ category }}
              </q-chip>
            </div>
          </div>

          <!-- actual contents goes into here -->
          <div id="tutorial-content-wrapper">
            <MarkdownSection
              :input-html="htmlContent"
              :breakpoint-react="true"
              :picture-zoom="true"
              :highlight="true"
              @breakpointClicked="
                (position) => {
                  $emit('breakpointClicked', position);
                }
              "
              @pictureZoomRequest="setRequestPictureIndex"
              @updatePictureSrcList="changePictureList"
            />
            <MarkdownPictureDisplay
              :photo-list="currentPictureList"
              :photo-index="currentPictureIndex"
              :display="currentDisplayState"
              @pictureDisplayChange="changeDisplayState"
              @pictureIndexUpdate="changeCurrentPictureIndex"
            />
          </div>

          <LicenseCard></LicenseCard>
        </div>
      </div>
    </q-scroll-area>

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
  import PictureDisplayMixin from '@/components/framework/md/PictureDisplayMixin';

  export default {
    mixins: [PictureDisplayMixin],
    metaInfo() {
      const articleTitle = this.headerTitle;
      return { title: articleTitle };
    },
    components: {
      MarkdownPictureDisplay: () =>
        import('@/components/framework/md/MarkdownPictureDisplay'),
      MarkdownSection,
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
      LicenseCard: () => import('@/components/framework/LicenseCard.vue'),
    },
    data() {
      return {
        articleViewPercentage_: 0,
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
      articleViewPercentage: {
        get() {
          return this.articleViewPercentage_;
        },
        set(d) {
          this.articleViewPercentage_ = d;
        },
      },
    },
    methods: {
      toLocalDateString,
      updateViewPercentage(info) {
        this.articleViewPercentage = info.verticalPercentage;
      },
      share() {
        saveTextToClipboard(window.location.href);
        // TODO use uniform notify
        successDialog({ message: 'The URL of this tutorial is copied.' });
      },
      scrollToTop() {
        if (this.$refs.tutorialScrollArea) {
          this.$refs.tutorialScrollArea.setScrollPosition(0, 300);
        }
      },
    },
  };
</script>

<style lang="sass">
  @import '~@quasar/extras/animate/zoomIn.css'
  @import '~@quasar/extras/animate/zoomOut.css'
  @import "~@/styles/article.sass"

  #scroll-up-icon:hover
    cursor: pointer
</style>
