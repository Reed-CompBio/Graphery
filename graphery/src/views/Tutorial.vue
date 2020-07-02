<template>
  <!-- TODO change list and app bar color -->
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
          separator-class="resizable-h-separator-splitter zero-z-index-separator"
          :separator-style="tutorialHorizontalSeparatorStyle"
          class="overflow-visible-splitter"
        >
          <template v-slot:before>
            <CytoscapeWrapper
              ref="cytoscapeWrapper"
              style="overflow-y: hidden;"
            ></CytoscapeWrapper>
          </template>
          <template v-slot:separator>
            <div :style="tutorialHorizontalSeparatorIconStyle"></div>
          </template>
          <template v-slot:after>
            <EditorWrapper
              ref="editorWrapper"
              class="full-height"
              @updateCyWithVarObj="updateCytoscapeWithVarObj"
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
  import { apiCaller } from '../services/apis';
  import { pullTutorialDetailQuery } from '../services/queries';

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
      ...mapActions('tutorials', ['clearAll', 'loadTutorial']),
      updateTutorialContent() {
        console.debug('API calls to get details of the tutorial');
        apiCaller(pullTutorialDetailQuery, {
          url: this.name,
          translation: this.$i18n.locale,
          default: 'en-us',
        })
          .then(([data, errors]) => {
            if (errors !== undefined || !data) {
              console.log(errors);
              // TODO throw error here
            }

            this.loadTutorial(data.tutorial);
          })
          .catch((err) => {
            // TODO in error
          });
        // 1. API calls to get page conentent
        // 2. Extract articles and graph info, turn off loading for the article section and load article
        // 3. API calls using graph info to get graphs
        // 4. Extract graphs details , turn off loading for the graph section and load graphs
        // 5. (think about mini editor, how to manage the data in the backend)
      },
      updateCytoscapeWithVarObj(varObj) {
        this.$refs.cytoscapeWrapper.highlightVarObj(varObj);
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
  .zero-z-index-separator
    z-index: 0
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
