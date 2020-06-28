<template>
  <div style="overflow: hidden;">
    <q-splitter
      v-if="notTortureSmallScreen"
      v-model="splitPos"
      :style="tutorialStyle"
      :horizontal="$q.screen.lt.md"
      separator-class="bg-light-blue"
      separator-style="width: 4px"
    >
      <template v-slot:before>
        <q-splitter
          v-model="editorSplitPos"
          horizontal
          separator-class="bg-light-blue"
          separator-style="width: 4px"
        >
          <template v-slot:before>
            <CytoscapeWrapper ref="cytoscapeWrapper"></CytoscapeWrapper>
          </template>
          <template v-slot:separator>
            <q-avatar
              color="primary"
              text-color="white"
              size="20px"
              icon="mdi-drag"
            />
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
      <template v-slot:separator>
        <q-avatar
          color="primary"
          text-color="white"
          size="32px"
          icon="mdi-drag"
        />
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
