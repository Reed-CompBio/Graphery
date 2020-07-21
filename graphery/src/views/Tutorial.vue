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
              v-show="currentTab === 'editor'"
              ref="editorWrapper"
              class="full-height"
              @updateCyWithVarObj="updateCytoscapeWithVarObj"
            ></EditorWrapper>
            <GraphInfo
              v-show="currentTab === 'graph-info'"
              :graphName="graphTitle"
              :isPublished="isGraphPublished"
              :abstract="graphAbstract"
            ></GraphInfo>
            <HowToHelper v-show="currentTab === 'how-to'"></HowToHelper>
            <!-- page sticky -->
            <q-page-sticky
              v-if="$q.screen.gt.xs"
              position="bottom-left"
              :offset="[30, 30]"
            >
              <q-fab
                direction="up"
                color="primary"
                icon="more_horiz"
                padding="10px"
              >
                <q-fab-action
                  color="accent"
                  icon="mdi-code-json"
                  padding="10px"
                  @click.prevent="switchTabView('editor')"
                >
                  <SwitchTooltip
                    :text="$t('tooltips.editor')"
                    self="center left"
                    anchor="center right"
                  />
                </q-fab-action>
                <q-fab-action
                  color="positive"
                  icon="info"
                  padding="10px"
                  @click.prevent="switchTabView('graph-info')"
                >
                  <SwitchTooltip
                    :text="$t('tooltips.graphInfo')"
                    self="center left"
                    anchor="center right"
                  />
                </q-fab-action>
                <q-fab-action
                  color="orange"
                  icon="help"
                  padding="10px"
                  @click.prevent="switchTabView('how-to')"
                >
                  <SwitchTooltip
                    :text="$t('tooltips.howTo')"
                    self="center left"
                    anchor="center right"
                  />
                </q-fab-action>
                <!-- TODO added graph info and how to use editor here -->
                <template v-slot:tooltip>
                  <SwitchTooltip
                    :text="$t('tooltips.showEditorAndMore')"
                    self="center left"
                    anchor="center right"
                  ></SwitchTooltip>
                </template>
              </q-fab>
            </q-page-sticky>
          </template>
        </q-splitter>
      </template>
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
    <!-- view for small screen -->
    <TutorialArticle v-else></TutorialArticle>
  </div>
</template>

<script>
  import { headerSize } from '../store/states/meta';
  import { mapState, mapActions, mapGetters } from 'vuex';
  import { apiCaller } from '../services/apis';
  import { pullTutorialDetailQuery } from '../services/queries';
  import { errorDialog } from '../services/helpers';

  export default {
    props: ['url'],
    components: {
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
      TutorialArticle: () =>
        import('@/components/tutorial/TutorialArticle.vue'),
      EditorWrapper: () => import('@/components/tutorial/EditorWrapper.vue'),
      GraphInfo: () => import('@/components/tutorial/GraphInfo.vue'),
      HowToHelper: () => import('@/components/tutorial/HowToHelper.vue'),
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
    },
    data() {
      return {
        editorSplitPos: 60,
        tutorialSeparatorWidth: 8, // px
        tutorialSeparatorIconSize: 4, // px
        tutorialSeparatorIconLength: 10, // %
        currentTab: 'editor',
      };
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
      ...mapGetters('tutorials', ['currentGraphContent']),
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
      graphTitle() {
        if (this.currentGraphContent) {
          return this.currentGraphContent.title;
        }
        return '';
      },
      isGraphPublished() {
        if (this.currentGraphContent) {
          return this.currentGraphContent.isPublished;
        }
        return false;
      },
      graphAbstract() {
        if (this.currentGraphContent) {
          return this.currentGraphContent.abstract;
        }
        return '';
      },
    },
    methods: {
      ...mapActions('tutorials', ['clearAll', 'loadTutorial']),
      updateTutorialContent() {
        console.debug(
          'API calls to get details of the tutorial with url',
          this.url
        );
        apiCaller(pullTutorialDetailQuery, {
          url: this.url,
          translation: this.$i18n.locale,
          default: 'en-us',
        })
          .then(([data, errors]) => {
            if (errors) {
              throw Error(
                'Invalid Data Received! Please Contact The Developer:' +
                  errors[0].message
              );
            }

            this.loadTutorial(data.tutorial);
          })
          .catch((err) => {
            errorDialog({
              message: 'An error occurs during pulling tutorials. ' + err,
            });
          });
      },
      updateCytoscapeWithVarObj(varObj) {
        this.$refs.cytoscapeWrapper.highlightVarObj(varObj);
      },
      switchTabView(tab) {
        this.currentTab = tab;
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
