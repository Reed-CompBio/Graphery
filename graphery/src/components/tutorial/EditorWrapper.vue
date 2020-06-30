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
        :label-value="`${sliderPos}/${sliderLength}`"
        :max="sliderLength"
        :step="1"
        snap
        dense
        style="width: 40%;"
        :label-always="showLabelAlways"
        :disable="disableStepSlider"
        @change="updateInfoFromSliderChange"
      ></q-slider>
      <!-- TODO  get the button actions done -->
      <!-- stepper button group -->
      <q-btn-group flat class="q-mr-md">
        <q-btn dense @click="showLabelAlwaysSwitch">
          <q-icon
            :name="
              showLabelAlways ? 'mdi-label-off-outline' : 'mdi-label-outline'
            "
          ></q-icon>
          <SwitchTooltip :text="$t('tooltips.showLabelAlways')"></SwitchTooltip>
        </q-btn>
        <!--        <div>-->
        <q-btn
          dense
          icon="mdi-skip-backward"
          @click="previousSeveralSteps"
          :disable="isPreviousButtonDisable"
        >
          <SwitchTooltip :text="$t('tooltips.fiveStepsBack')"></SwitchTooltip>
        </q-btn>
        <q-btn
          dense
          icon="mdi-skip-previous"
          @click="previousStep"
          :disable="isPreviousButtonDisable"
        >
          <SwitchTooltip :text="$t('tooltips.oneStepBack')"></SwitchTooltip>
        </q-btn>
        <!--        </div>-->
        <q-btn dense :icon="playPauseButton" :disable="isNextButtonDisable">
          <SwitchTooltip :text="$t('tooltips.autoRun')"></SwitchTooltip>
        </q-btn>
        <!--        <div>-->
        <q-btn
          dense
          icon="mdi-skip-next"
          @click="nextStep"
          :disable="isNextButtonDisable"
        >
          <SwitchTooltip :text="$t('tooltips.oneStepForward')"></SwitchTooltip>
        </q-btn>
        <q-btn
          dense
          icon="mdi-skip-forward"
          @click="nextSeveralSteps"
          :disable="isNextButtonDisable"
        >
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
          <q-card class="popup-wrapper full-height" style="overflow-y: hidden;">
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
        showLabelAlways: true,
        sliderPos: 1,
        codeValueListSplitPos: (5 / 6) * 100,
        advanceSteps: 5,
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
        return this.resultJsonArr.length;
      },
      disableStepSlider() {
        return this.sliderLength < 1;
      },
      resultJsonArrPos() {
        return this.sliderPos - 1;
      },
      isNextButtonDisable() {
        return !this.isWalkable();
      },
      isPreviousButtonDisable() {
        return !this.isWalkable(-1);
      },
    },
    methods: {
      ...mapActions('tutorials', ['loadVariableList']),
      switchTabView(tabName) {
        this.routerViewName = tabName;
      },
      showLabelAlwaysSwitch() {
        this.showLabelAlways = !this.showLabelAlways;
      },
      // Stepper button actions
      isWalkable(deltaStep = 1) {
        return (
          !this.disableStepSlider &&
          1 <= this.sliderPos + deltaStep &&
          this.sliderPos + deltaStep <= this.sliderLength
        );
      },
      incrementSliderPos(deltaPos = 1) {
        if (this.isWalkable(deltaPos)) {
          this.sliderPos += deltaPos;
          return true;
        }
        return false;
      },
      loadNextVariableState(variableState) {
        if (variableState) {
          this.loadVariableList(variableState);
        }
      },
      loadInfo(lineObject) {
        this.$refs.editorComponent.moveToLine(lineObject['line']);
        this.loadNextVariableState(lineObject['variables']);
        this.$emit('updateCyWithVarObj', lineObject['variables']);
      },
      getTheLastState(index) {
        if (this.resultJsonArr) {
          for (let i = index; i >= 0; i--) {
            const lineObject = this.resultJsonArr[i];
            if (lineObject['variables']) {
              return lineObject;
            }
          }
          // Which should never happen since the backend ensures the first element must have a var dict
          throw Error(
            'The execution result json is not valid. Please send a feedback to the developer.'
          );
        }

        return null;
      },
      initWrapperState() {
        // called after the api call
        // TODO editor load line
        if (this.resultJsonArr) {
          this.loadInfo(this.resultJsonArr[0]);
        }
      },
      previousSeveralSteps() {
        if (this.resultJsonArr) {
          if (!this.incrementSliderPos(-this.advanceSteps)) {
            this.sliderPos = 0;
          }
          const previousLineObj = this.getTheLastState(this.resultJsonArrPos);
          this.loadInfo(previousLineObj);
        }
      },
      previousStep() {
        if (this.resultJsonArr && this.incrementSliderPos(-1)) {
          const previousLineObj = this.resultJsonArr[this.resultJsonArrPos];
          this.loadInfo(previousLineObj);
        }
      },
      // TODO something wrong here
      nextStep() {
        if (this.resultJsonArr && this.incrementSliderPos()) {
          const nextLineObj = this.resultJsonArr[this.resultJsonArrPos];
          this.loadInfo(nextLineObj);
        }
      },
      nextSeveralSteps() {
        if (this.resultJsonArr) {
          if (!this.incrementSliderPos(this.advanceSteps)) {
            this.sliderPos = this.sliderLength;
          }
          const nextLineObj = this.getTheLastState(this.resultJsonArrPos);
          this.loadInfo(nextLineObj);
        }
      },
      updateInfoFromSliderChange(posValue) {
        const arrIndex = posValue - 1;
        const lineObject = this.getTheLastState(arrIndex);
        this.loadInfo(lineObject);
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
