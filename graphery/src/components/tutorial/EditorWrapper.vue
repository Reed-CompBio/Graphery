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
        <q-btn dense :icon="playPauseButton">
          <!--          <SwitchTooltip :text="$t('tooltips.autoRun')"></SwitchTooltip>-->
          <SwitchTooltip
            :text="$t('tooltips.notAvailableCurrently')"
          ></SwitchTooltip>
        </q-btn>
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
      <q-btn-group flat class="q-mr-md">
        <q-btn dense disable>
          <q-icon name="mdi-cloud-upload" />
          <SwitchTooltip
            :text="$t('tooltips.runCodeOnTheCloud')"
          ></SwitchTooltip>
        </q-btn>
        <q-btn
          dense
          :disable="!enableEditing"
          @click.prevent="pushCodeToExecute"
        >
          <q-icon name="mdi-cloud-download" />
          <SwitchTooltip :text="$t('tooltips.runCodeLocally')"></SwitchTooltip>
        </q-btn>
      </q-btn-group>

      <!-- copy paste button group -->
      <q-btn-group flat class="q-mr-md">
        <q-btn dense icon="mdi-content-copy" @click="copyCurrentCode">
          <SwitchTooltip :text="$t('tooltips.copyCodes')"></SwitchTooltip>
        </q-btn>
        <q-btn
          dense
          icon="mdi-content-paste"
          @click="setCurrentCodeFromClipboard"
        >
          <SwitchTooltip :text="$t('tooltips.pasteCodes')"></SwitchTooltip>
        </q-btn>
      </q-btn-group>

      <q-btn-group flat class="q-mr-md">
        <q-btn
          dense
          icon="mdi-folder-network-outline"
          :disable="true"
          @click="openWorkSpaceSelection"
        ></q-btn>
      </q-btn-group>

      <!-- Editor status -->
      <q-btn-group flat class="q-mr-md">
        <q-btn dense disable :icon="enableEditing ? 'lock_open' : 'lock'">
        </q-btn>
        <SwitchTooltip
          :text="$t('tooltips.goToSettingsToChangeEditingPermission')"
        ></SwitchTooltip>
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
    <!--    <q-dialog v-model="isWorkSpaceSelectionOpen">-->
    <!--      <q-card>-->
    <!--        <q-toolbar>-->
    <!--          <TutorialWorkSpaceController-->
    <!--            style="width: 30%"-->
    <!--            class="q-mr-md"-->
    <!--          ></TutorialWorkSpaceController>-->
    <!--          <q-space />-->
    <!--          <q-btn flat round dense icon="close" v-close-popup />-->
    <!--        </q-toolbar>-->

    <!--        <q-drawer :v-model="true" persistent bordered>-->
    <!--          <q-list>-->
    <!--            <q-item v-for="i in [1, 2, 3]" :key="i">-->
    <!--              {{ i }}-->
    <!--            </q-item>-->
    <!--          </q-list>-->
    <!--        </q-drawer>-->
    <!--        <q-card-section>-->
    <!--          Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum-->
    <!--          repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis-->
    <!--          perferendis totam, ea at omnis vel numquam exercitationem aut, natus-->
    <!--          minima, porro labore.-->
    <!--        </q-card-section>-->
    <!--      </q-card>-->
    <!--    </q-dialog>-->
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapState } from 'vuex';
  import { saveTextToClipboard } from '../../services/helpers.ts';
  import { localServerCaller } from '../../services/apis';

  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
      Editor: () => import('@/components/tutorial/Editor.vue'),
      VariableList: () => import('@/components/tutorial/VariableList.vue'),
      // TutorialWorkSpaceController: () =>
      //   import('@/components/tutorial/TutorialWorkSpaceController.vue'),
    },
    data() {
      return {
        routerViewName: 'editor',
        isPlaying: false,
        showLabelAlways: true,
        sliderPos: 1,
        codeValueListSplitPos: (5 / 6) * 100,
        advanceSteps: 5,
        isWorkSpaceSelectionOpen: false,
      };
    },
    computed: {
      ...mapGetters('tutorials', [
        'resultJsonArrEmpty',
        'variableObjEmpty',
        'resultJsonArr',
      ]),
      ...mapState('settings', ['enableEditing']),
      playPauseButton() {
        if (this.isPlaying) {
          return 'mdi-pause';
        } else {
          return 'mdi-play';
        }
      },
      sliderLength() {
        if (this.resultJsonArr) {
          return this.resultJsonArr.length;
        }
        return 0;
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
      ...mapActions('tutorials', ['loadVariableObj', 'loadCustomJson']),
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
          this.loadVariableObj(variableState);
        }
      },
      loadInfo(lineObject) {
        this.$refs.editorComponent.moveToLine(lineObject['line']);
        this.loadNextVariableState(lineObject['variables']);
        this.$emit('updateCyWithVarObj', lineObject['variables']);
      },
      getTheLastState(index) {
        if (!this.resultJsonArrEmpty) {
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
        if (this.resultJsonArr && !this.resultJsonArrEmpty) {
          this.loadInfo(this.resultJsonArr[0]);
        }
      },
      previousSeveralSteps() {
        if (!this.resultJsonArrEmpty) {
          if (!this.incrementSliderPos(-this.advanceSteps)) {
            this.sliderPos = 0;
          }
          const previousLineObj = this.getTheLastState(this.resultJsonArrPos);
          this.loadInfo(previousLineObj);
        }
      },
      previousStep() {
        if (!this.resultJsonArrEmpty && this.incrementSliderPos(-1)) {
          const previousLineObj = this.resultJsonArr[this.resultJsonArrPos];
          this.loadInfo(previousLineObj);
        }
      },
      // TODO something wrong here
      nextStep() {
        if (!this.resultJsonArrEmpty && this.incrementSliderPos()) {
          const nextLineObj = this.resultJsonArr[this.resultJsonArrPos];
          this.loadInfo(nextLineObj);
        }
      },
      nextSeveralSteps() {
        if (!this.resultJsonArrEmpty) {
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
      reloadStepper() {
        this.sliderPos = 1;
        this.loadVariableObj(null);
      },
      getCurrentCode() {
        return this.$refs.editorComponent.content;
      },
      copyCurrentCode() {
        if (this.$refs.editorComponent) {
          saveTextToClipboard(this.getCurrentCode());
        }
      },
      setCurrentCodeFromClipboard() {
        navigator.clipboard
          .readText()
          .then((text) => {
            if (this.$refs.editorComponent) {
              this.$refs.editorComponent.setCodeContent(text);
            }
          })
          .catch((err) => {
            console.error('Failed to read clipboard contents: ', err);
          });
      },
      pushCodeToExecute() {
        localServerCaller(
          this.getCurrentCode(),
          this.$store.getters['tutorials/currentGraphJsonObj']
        ).then((data) => {
          this.reloadStepper();

          if (data['error'] || !('data' in data)) {
            // TODO handle error
          }

          const { codeHash, execResult } = data['data'];
          // TODO link this with workspace

          console.debug(codeHash, execResult);
          this.loadCustomJson(execResult);

          // TODO use it to pass the actual content
        });
      },
      openWorkSpaceSelection() {
        this.isWorkSpaceSelectionOpen = true;
      },
    },
    watch: {
      resultJsonArr: function() {
        this.reloadStepper();
        this.initWrapperState();
      },
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
