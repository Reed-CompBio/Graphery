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
    <!-- stepper button group -->
    <q-btn-group flat class="q-mr-md">
      <q-btn dense @click="showLabelAlwaysSwitch">
        <q-icon
          :name="
            sliderLabelAlways ? 'mdi-label-off-outline' : 'mdi-label-outline'
          "
        ></q-icon>
        <SwitchTooltip :text="$t('tooltips.showLabelAlways')"></SwitchTooltip>
      </q-btn>
      <q-btn
        dense
        icon="mdi-skip-backward"
        @click="onMultipleStepsBack"
        :disable="isPreviousButtonDisable"
      >
        <SwitchTooltip :text="$t('tooltips.fiveStepsBack')"></SwitchTooltip>
      </q-btn>
      <q-btn
        dense
        icon="mdi-skip-previous"
        @click="onStepBack"
        :disable="isPreviousButtonDisable"
      >
        <SwitchTooltip :text="$t('tooltips.oneStepBack')"></SwitchTooltip>
      </q-btn>
      <q-btn
        dense
        icon="mdi-play"
        @click="onAutoRun"
        :disable="isNextButtonDisable"
      >
        <SwitchTooltip :text="$t('tooltips.autoRun')"></SwitchTooltip>
      </q-btn>
      <q-btn
        dense
        icon="mdi-skip-next"
        @click="onStepForward"
        :disable="isNextButtonDisable"
      >
        <SwitchTooltip :text="$t('tooltips.oneStepForward')"></SwitchTooltip>
      </q-btn>
      <q-btn
        dense
        icon="mdi-skip-forward"
        @click="onMultipleStepForward"
        :disable="isNextButtonDisable"
      >
        <SwitchTooltip :text="$t('tooltips.fiveStepsForward')"></SwitchTooltip>
      </q-btn>
      <!-- TODO auto play maybe?  -->
    </q-btn-group>

    <!-- execution button group -->
    <q-btn-group flat class="q-mr-md">
      <q-btn
        dense
        icon="mdi-cloud-upload"
        :disable="isExecButtonDisable"
        @click="onPushToCloudExec"
        :loading="execLoading"
      >
        <SwitchTooltip :text="$t('tooltips.runCodeOnTheCloud')"></SwitchTooltip>
      </q-btn>
      <q-btn
        dense
        icon="mdi-cloud-download"
        :disable="isExecButtonDisable"
        @click.prevent="onPushToLocalExec"
        :loading="execLoading"
      >
        <SwitchTooltip :text="$t('tooltips.runCodeLocally')"></SwitchTooltip>
      </q-btn>
    </q-btn-group>

    <!-- copy paste button group -->
    <q-btn-group flat class="q-mr-md">
      <q-btn dense icon="mdi-content-copy" @click="onCopyCurrentCode">
        <SwitchTooltip :text="$t('tooltips.copyCodes')" />
      </q-btn>
      <q-btn dense icon="mdi-content-paste" @click="onPasteFromClipboard">
        <SwitchTooltip :text="$t('tooltips.pasteCodes')" />
      </q-btn>
      <q-btn
        dense
        icon="mdi-rotate-right-variant"
        @click="onChangeVariableListOrientation"
      >
        <SwitchTooltip :text="$t('tooltips.changeVariableListOrientation')" />
      </q-btn>
    </q-btn-group>

    <q-btn-group flat class="q-mr-md">
      <q-btn dense icon="mdi-folder-network-outline" @click="onCallWorkSpace">
        <SwitchTooltip :text="$t('tooltips.openWorkSpace')" />
      </q-btn>
    </q-btn-group>

    <!-- Editor status -->
    <q-btn-group flat class="q-mr-md">
      <q-btn
        dense
        disable
        :icon="$store.state.settings.enableEditing ? 'lock_open' : 'lock'"
      >
      </q-btn>
      <SwitchTooltip
        :text="$t('tooltips.goToSettingsToChangeEditingPermission')"
      ></SwitchTooltip>
    </q-btn-group>
  </q-bar>
</template>

<script>
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
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
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
        this.setSliderPosition(this.getSliderPosition - this.skipSteps);
      },
      onStepBack() {
        this.setSliderPosition(this.getSliderPosition - 1);
      },
      onAutoRun() {
        // TODO
      },
      onStepForward() {
        this.setSliderPosition(this.getSliderPosition + 1);
      },
      onMultipleStepForward() {
        this.setSliderPosition(this.getSliderPosition + this.skipSteps);
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
      onCallWorkSpace() {
        this.$emit('onCallWorkSpace');
      },
    },
  };
</script>
