<template>
  <!-- change list and app bar color -->
  <div style="overflow: hidden;">
    <q-splitter
      v-if="notTortureSmallScreen"
      v-model="splitPos"
      :style="tutorialStyle"
      :horizontal="$q.screen.lt.md"
      :separator-class="
        $q.screen.lt.md
          ? 'resizable-h-separator-splitter'
          : 'resizable-v-separator-splitter'
      "
      :separator-style="
        $q.screen.lt.md
          ? tutorialHorizontalSeparatorStyle
          : tutorialVerticalSeparatorStyle
      "
      class="overflow-hidden-splitter"
    >
      <template v-slot:before>
        <q-splitter
          id="graph-code-section"
          v-model="editorSplitPos"
          horizontal
          separator-class="resizable-h-separator-splitter"
          :separator-style="tutorialHorizontalSeparatorStyle"
          class="overflow-visible-splitter"
        >
          <template v-slot:before>
            <CytoscapeWrapper ref="cytoscapeWrapper"></CytoscapeWrapper>
          </template>
          <template v-slot:separator>
            <div :style="tutorialHorizontalSeparatorIconStyle"></div>
          </template>
          <template v-slot:after>
            <EditorWrapper
              ref="editorWrapper"
              v-if="notTortureSmallScreen"
              class="full-height"
            ></EditorWrapper>
          </template>
        </q-splitter>
      </template>
      <!-- TODO 放大缩小 -->
      <template v-slot:separator>
        <div
          :style="tutorialHorizontalSeparatorIconStyle"
          v-if="$q.screen.lt.md"
        ></div>
        <div :style="tutorialVerticalSeparatorIconStyle" v-else></div>
      </template>
      <template v-slot:after>
        <TutorialArticle class="full-height"></TutorialArticle>
      </template>
    </q-splitter>
    <TutorialArticle v-else></TutorialArticle>
  </div>
</template>

<script>
  import { headerSize } from '../store/states/meta';
  import { mapActions, mapState } from 'vuex';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
      TutorialArticle: () =>
        import('@/components/tutorial/TutorialArticle.vue'),
      EditorWrapper: () => import('@/components/tutorial/EditorWrapper.vue'),
    },
    data() {
      return {
        editorSplitPos: 60,
        tutorialSeparatorWidth: 8, // px
        tutorialSeparatorIconSize: 4, // px
        tutorialSeparatorIconLength: 10, // %
      };
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
      splitPos: {
        set(d) {
          this.$store.dispatch(
            'settings/changeGraphSplitPos',
            Math.round(d * 10) / 10
          );
        },
        get() {
          return this.graphSplitPos;
        },
      },
      tutorialStyle() {
        return {
          height: `calc(100vh - ${headerSize}px)`,
        };
      },
      tutorialHorizontalSeparatorStyle() {
        return {
          height: `${this.tutorialSeparatorWidth}px`,
        };
      },
      tutorialVerticalSeparatorStyle() {
        return {
          width: `${this.tutorialSeparatorWidth}px`,
        };
      },
      tutorialHorizontalSeparatorIconStyle() {
        return {
          'border-top': `${this.tutorialSeparatorIconSize}px solid #b3b3b3`,
          'border-radius': '25px',
          width: `${this.tutorialSeparatorIconLength}%`,
        };
      },
      tutorialVerticalSeparatorIconStyle() {
        return {
          'border-left': `${this.tutorialSeparatorIconSize}px solid #b3b3b3`,
          'border-radius': '25px',
          height: `${this.tutorialSeparatorIconLength}%`,
        };
      },
      notTortureSmallScreen() {
        return this.$q.screen.gt.xs;
      },
    },
    methods: {
      ...mapActions('tutorials', ['clearAll']),
      updateTutorialContent() {
        console.log('API calls to get details of the tutorial');
        // TODO
        // 1. API calls to get page conentent
        // 2. Extract articles and graph info, turn off loading for the article section and load article
        // 3. API calls using graph info to get graphs
        // 4. Extract graphs details , turn off loading for the graph section and load graphs
        // 5. (think about mini editor, how to manage the data in the backend)
      },
    },
    watch: {
      name: function(newVal, oldVal) {
        // ensures page updating when the url is changed
        // TODO I don't think I need this
        console.log(`route change from ${oldVal} to ${newVal}`);
        this.updateTutorialContent();
      },
    },
    mounted() {
      if (this.$q.screen.lt.sm) {
        this.$q.notify({
          multiLine: true,
          message: this.$t('notify.mobileWarning'),
          icon: 'warning',
          actions: [{}],
        });
      } else {
        this.$q.notify({
          multiLine: true,
          message: this.$t('notify.editorEntry'),
          icon: 'mdi-code-json',
          timeout: 1500,
        });
      }
      // TODO add a setting to hide notification
      if (this.$q.platform.is.mobile && this.$q.platform.is.chrome) {
        // TODO temporary workaround, find a way to solve mobile viewport
        this.$q.notify({
          multiLine: true,
          message: this.$t('notify.mobileChromeWarning'),
          icon: 'warning',
        });
      }

      // pull tutorials
      this.updateTutorialContent();
    },
    destroyed() {
      this.clearAll();
      // TODO restore states in vuex
    },
  };
</script>

<style lang="sass">
  .overflow-visible-splitter > .q-splitter__after
    overflow: visible
  .overflow-hidden-splitter > .q-splitter__before
    overflow: hidden
  .resizable-h-separator-splitter:hover, .resizable-v-separator-splitter:hover
    transform: scale(1.5)
  .resizable-h-separator-splitter, .resizable-v-separator-splitter
    transition: 300ms ease-out
  .resizable-h-separator-splitter:hover
    height: 12px
  .resizable-v-separator-splitter:hover
    width: 12px
</style>
