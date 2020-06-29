<template>
  <div id="editor-container">
    <q-bar>
      <q-icon name="mdi-function" />
      <div style="text-transform: uppercase;">{{ routerViewName }}</div>
      <q-space />
      <q-slider
        id="stepper-slider"
        v-model="sliderPos"
        :min="1"
        label
        :max="sliderLength"
        :step="1"
        snap
        dense
        style="width: 40%;"
        label-always
        :disable="disableStepSlider"
      ></q-slider>
      <!-- TODO  get the button actions done -->
      <!-- stepper button group -->
      <q-btn-group flat class="q-mr-md">
        <!--        <div>-->
        <q-btn dense icon="mdi-skip-backward">
          <SwitchTooltip :text="$t('tooltips.fiveStepsBack')"></SwitchTooltip>
        </q-btn>
        <q-btn dense icon="mdi-skip-previous">
          <SwitchTooltip :text="$t('tooltips.oneStepBack')"></SwitchTooltip>
        </q-btn>
        <!--        </div>-->
        <q-btn dense :icon="playPauseButton">
          <SwitchTooltip :text="$t('tooltips.autoRun')"></SwitchTooltip>
        </q-btn>
        <!--        <div>-->
        <q-btn dense icon="mdi-skip-next" @click="nextStep">
          <SwitchTooltip :text="$t('tooltips.oneStepForward')"></SwitchTooltip>
        </q-btn>
        <q-btn dense icon="mdi-skip-forward">
          <SwitchTooltip
            :text="$t('tooltips.fiveStepsForward')"
          ></SwitchTooltip>
        </q-btn>
        <!-- TODO auto play maybe?  -->
      </q-btn-group>
      <!-- execution button group -->
      <q-btn-group flat class="q-mr-md" v-touch-pan.prevent.mouse="null">
        <q-btn dense>
          <q-icon name="mdi-cloud-upload" />
          <SwitchTooltip
            :text="$t('tooltips.runCodeOnTheCloud')"
          ></SwitchTooltip>
        </q-btn>
        <q-btn dense>
          <q-icon name="mdi-cloud-download" />
          <SwitchTooltip :text="$t('tooltips.runCodeLocally')"></SwitchTooltip>
        </q-btn>
      </q-btn-group>
      <!-- copy paste button group -->
      <q-btn-group flat class="q-mr-md">
        <q-btn dense icon="mdi-content-copy">
          <SwitchTooltip :text="$t('tooltips.copyCodes')"></SwitchTooltip>
        </q-btn>
        <q-btn dense icon="mdi-content-paste">
          <SwitchTooltip :text="$t('tooltips.pasteCodes')"></SwitchTooltip>
        </q-btn>
      </q-btn-group>
    </q-bar>
    <div class="row" style="height: calc(100% - 32px); overflow: hidden;">
      <q-splitter
        v-model="codeValueListSplitPos"
        separator-class="resizable-v-separator-splitter"
        separator-style="width: 4px;"
        class="full-height full-width"
      >
        <template v-slot:before>
          <q-card class="popup-wrapper full-height">
            <Editor ref="editorComponent" class="full-height"></Editor>
            <!--          <router-view class="full-height" :name="routerViewName"></router-view>-->
            <!-- TODO use child router link instead of tab panel -->
            <!-- TODO use q-fab instead of sticky -->
          </q-card>
        </template>
        <template v-slot:separator>
          <div
            style="border-left: 4px solid rgb(179, 179, 179); border-radius: 25px; height: 10%;"
          ></div>
        </template>
        <template v-slot:after>
          <VariableList></VariableList>
        </template>
      </q-splitter>
    </div>
    <!-- page sticky button -->
    <!--    <q-page-sticky-->
    <!--      v-if="$q.screen.gt.xs"-->
    <!--      position="bottom-left"-->
    <!--      :offset="[30, 30]"-->
    <!--    >-->
    <!--      <q-fab direction="up" color="primary" icon="more_horiz">-->
    <!--        <q-fab-action-->
    <!--          color="secondary"-->
    <!--          icon="mdi-code-json"-->
    <!--          @click.prevent="switchTabView('editor')"-->
    <!--        />-->
    <!--        <q-fab-action-->
    <!--          color="skyblue"-->
    <!--          icon="block"-->
    <!--          @click.prevent="switchTabView('block')"-->
    <!--        />-->
    <!--      </q-fab>-->
    <!--      &lt;!&ndash; TODO change the translation &ndash;&gt;-->
    <!--      <SwitchTooltip :text="$t('tooltips.showEditorAndMore')"></SwitchTooltip>-->
    <!--      &lt;!&ndash;      <q-btn round color="primary" icon="mdi-code-json" @click="toggleEditor" />&ndash;&gt;-->
    <!--    </q-page-sticky>-->
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex';

  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
      Editor: () => import('@/components/tutorial/Editor.vue'),
      VariableList: () => import('@/components/tutorial/VariableList.vue'),
    },
    data() {
      return {
        routerViewName: 'editor',
        isPlaying: false,
        sliderPos: 1,
        codeValueListSplitPos: (5 / 6) * 100,
      };
    },
    computed: {
      ...mapGetters('tutorials', [
        'resultJsonEmpty',
        'variableObjEmpty',
        'resultJsonArr',
      ]),

      playPauseButton() {
        if (this.isPlaying) {
          return 'mdi-pause';
        } else {
          return 'mdi-play';
        }
      },
      sliderLength() {
        return this.resultJsonArr.length + 1;
      },
      disableStepSlider() {
        return this.sliderLength === 1;
      },
      resultJsonArrPos() {
        return this.sliderPos - 1;
      },
    },
    methods: {
      ...mapActions('tutorials', ['loadVariableList']),
      switchTabView(tabName) {
        this.routerViewName = tabName;
      },
      // Stepper button actions
      notFull(deltaStep = 1) {
        return this.sliderPos + deltaStep <= this.sliderLength;
      },
      incrementSliderPos(deltaPos = 1) {
        this.sliderPos += deltaPos;
      },
      loadNextVariableState(variableState) {
        if (variableState) {
          this.loadVariableList(variableState);
        }
      },
      loadInfo(lineObject) {
        this.$refs.editorComponent.moveToLine(lineObject['line']);
        this.loadNextVariableState(lineObject['variables']);
      },
      initWrapperState() {
        // called after the api call
        if (this.resultJsonArr) {
          this.loadInfo(this.resultJsonArr[0]);
        }
      },
      nextStep() {
        if (this.resultJsonArr && this.notFull()) {
          this.incrementSliderPos();
          this.loadInfo(this.resultJsonArr[this.resultJsonArrPos]);
          // TODO editor load line
        }
      },
    },
    mounted() {
      setTimeout(() => {
        this.initWrapperState();
      }, 2000);
    },
  };
</script>

<style lang="sass">
  .q-tab-panel
    padding: 8px
  #editor-container
    position: absolute
    z-index: auto
    height: 100% !important
    width: 100% !important
  #stepper-slider .q-slider__pin
    z-index: 10
</style>
