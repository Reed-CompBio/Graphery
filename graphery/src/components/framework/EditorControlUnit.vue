<template>
  <q-bar>
    <q-icon name="mdi-function" />
    <div style="text-transform: uppercase;">Editor</div>
    <q-space />

    <q-slider
      id="stepper-slider"
      v-model="modelSliderPos"
      :min="1"
      label
      :label-value="`${getSliderPosition}/${sliderLength}`"
      :max="sliderLength"
      :step="1"
      snap
      dense
      style="width: 40%;"
      :label-always="sliderLabelAlways"
      :disable="disableStepSlider"
    ></q-slider>
    <!--    abcde FIXME-->
    <!-- FIXME: pop-up slider, style -->
    <!-- FIXME: middle, calc the width of editor -->
    <!-- stepper button group -->
    <q-btn-group flat class="q-mr-md">
      <div>
        <q-btn flat dense @click="showLabelAlwaysSwitch">
          <q-icon
            :name="
              sliderLabelAlways ? 'mdi-label-off-outline' : 'mdi-label-outline'
            "
          ></q-icon>
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.showLabelAlways')"></SwitchTooltip>
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-skip-backward"
          @click="onMultipleStepsBack"
          :disable="isPreviousButtonDisable"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.fiveStepsBack')"></SwitchTooltip>
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-skip-previous"
          @click="onStepBack"
          :disable="isPreviousButtonDisable"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.oneStepBack')"></SwitchTooltip>
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-skip-next"
          @click="onStepForward"
          :disable="isNextButtonDisable"
          :color="showNextStepBackground"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.oneStepForward')"></SwitchTooltip>
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-skip-forward"
          @click="onMultipleStepForward"
          :disable="isNextButtonDisable"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.fiveStepsForward')"></SwitchTooltip>
      </div>
      <!-- TODO auto play maybe?  -->
    </q-btn-group>

    <!-- execution button group -->
    <q-btn-group flat class="q-mr-md">
      <div>
        <q-btn
          flat
          dense
          icon="mdi-cloud-upload"
          :disable="isExecButtonDisable"
          @click="onPushToCloudExec"
          :loading="execLoading"
        >
          <SwitchTooltip
            :text="$t('tooltips.runCodeOnTheCloud')"
          ></SwitchTooltip>
        </q-btn>
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-cloud-download"
          :disable="isExecButtonDisable"
          @click.prevent="onPushToLocalExec"
          :loading="execLoading"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.runCodeLocally')"></SwitchTooltip>
      </div>
    </q-btn-group>

    <!-- copy paste button group -->
    <q-btn-group flat class="q-mr-md">
      <div>
        <q-btn flat dense icon="mdi-content-copy" @click="onCopyCurrentCode">
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.copyCodes')" />
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-content-paste"
          @click="onPasteFromClipboard"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.pasteCodes')" />
      </div>
      <div>
        <q-btn
          flat
          dense
          icon="mdi-rotate-right-variant"
          @click="onChangeVariableListOrientation"
        >
        </q-btn>
        <SwitchTooltip :text="$t('tooltips.changeVariableListOrientation')" />
      </div>
    </q-btn-group>

    <!--    <q-btn-group flat class="q-mr-md">-->
    <!--      <q-btn dense icon="mdi-folder-network-outline" @click="onCallWorkSpace">-->
    <!--        <SwitchTooltip :text="$t('tooltips.openWorkSpace')" />-->
    <!--      </q-btn>-->
    <!--    </q-btn-group>-->

    <!-- Editor status -->
    <q-btn-group flat class="q-mr-md">
      <q-btn
        dense
        @click="onEditingLockStateChange"
        :icon="$store.state.settings.enableEditing ? 'lock_open' : 'lock'"
      >
        <SwitchTooltip
          :text="$t('tooltips.goToSettingsToChangeEditingPermission')"
        />
      </q-btn>
    </q-btn-group>
  </q-bar>
</template>

<script>
  import SwitchTooltip from '@/components/framework/SwitchTooltip';
  export default {
    props: {
      sliderLength: {
        type: Number,
        default: 1,
      },
      disableOverride: {
        type: Boolean,
        default: false,
      },
      execLoading: {
        type: Boolean,
      },
    },
    components: {
      SwitchTooltip,
    },
    data() {
      return {
        sliderLabelAlways: true,
        skipSteps: 5,
        sliderPositionCopy: 1,
      };
    },
    computed: {
      modelSliderPos: {
        set(d) {
          this.sliderPositionCopy = d;
          this.$emit('onSliderChange', this.sliderPosToJsonPos(d));
        },
        get() {
          return this.sliderPositionCopy;
        },
      },
      isExecButtonDisable() {
        return this.disableOverride;
      },
      isPreviousButtonDisable() {
        return !this.isWalkable(-1);
      },
      isNextButtonDisable() {
        return !this.isWalkable();
      },
      disableStepSlider() {
        // TODO
        return this.disableOverride || this.sliderLength <= 1;
      },
      getSliderPosition() {
        return this.modelSliderPos;
      },
      showNextStepBackground() {
        if (this.getSliderPosition === 1) {
          return 'primary';
        } else {
          return undefined;
        }
      },
    },
    methods: {
      setSliderPosition(position) {
        this.modelSliderPos = position;
      },
      sliderPosToJsonPos(sliderPos) {
        return sliderPos - 1;
      },
      jsonPosToSliderPos(sliderPos) {
        return sliderPos + 1;
      },
      setPositionValueCopyFromJsonPos(jsonPos) {
        this.sliderPositionCopy = this.jsonPosToSliderPos(jsonPos);
      },
      isWalkable(deltaStep = 1) {
        return (
          !this.disableOverride &&
          1 <= this.getSliderPosition + deltaStep &&
          this.getSliderPosition + deltaStep <= this.sliderLength
        );
      },
      showLabelAlwaysSwitch() {
        this.sliderLabelAlways = !this.sliderLabelAlways;
      },
      onMultipleStepsBack() {
        const finalStep = this.getSliderPosition - this.skipSteps;
        this.setSliderPosition(finalStep < 1 ? 1 : finalStep);
      },
      onStepBack() {
        this.setSliderPosition(this.getSliderPosition - 1);
      },
      onStepForward() {
        this.setSliderPosition(this.getSliderPosition + 1);
      },
      onMultipleStepForward() {
        const finalStep = this.getSliderPosition + this.skipSteps;
        this.setSliderPosition(
          finalStep > this.sliderLength ? this.sliderLength : finalStep
        );
      },
      onPushToCloudExec() {
        this.$emit('onPushToCloudExec');
      },
      onPushToLocalExec() {
        this.$emit('onPushToLocalExec');
      },
      onCopyCurrentCode() {
        this.$emit('onCopyCurrentCode');
      },
      onPasteFromClipboard() {
        this.$emit('onPasteFromClipboard');
      },
      onChangeVariableListOrientation() {
        this.$emit('onChangeVariableListOrientation');
      },
      onEditingLockStateChange() {
        this.$store.dispatch(
          'settings/changeEnableEditing',
          !this.$store.getters['settings/getEnableEditing']
        );
      },
      // onCallWorkSpace() {
      //   this.$emit('onCallWorkSpace');
      // },
    },
  };
</script>

<style lang="sass" scoped></style>
