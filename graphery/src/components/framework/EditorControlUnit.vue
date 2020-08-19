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
      :label-value="`${modelSliderPos}/${sliderLength}`"
      :max="sliderLength"
      :step="1"
      snap
      dense
      style="width: 40%;"
      :label-always="sliderLabelAlways"
      :disable="disableStepSlider"
      @change="onSliderChange"
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
        icon="play"
        @click="notAvailableMessage"
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
      <q-btn dense icon="mdi-cloud-upload" @click="onPushToCloudExec">
        <SwitchTooltip :text="$t('tooltips.runCodeOnTheCloud')"></SwitchTooltip>
      </q-btn>
      <q-btn dense @click.prevent="onPushToLocalExec">
        <q-icon name="mdi-cloud-download" />
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
      <q-btn dense disable :icon="editorEnableEditing ? 'lock_open' : 'lock'">
      </q-btn>
      <SwitchTooltip
        :text="$t('tooltips.goToSettingsToChangeEditingPermission')"
      ></SwitchTooltip>
    </q-btn-group>
  </q-bar>
</template>

<script>
  import { notAvailableMessage } from '@/services/helpers';

  export default {
    props: {
      currentSliderPosition: {
        type: Number,
        default: 1,
      },
      sliderLength: {
        type: Number,
        default: 1,
      },
      disableOverride: {
        type: Boolean,
        default: false,
      },
      editorEnableEditing: {
        type: Boolean,
        default: false,
      },
    },
    model: {
      prop: 'currentSliderPosition',
      event: 'changeSliderPos',
    },
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
    },
    data() {
      return {
        sliderLabelAlways: true,
        skipSteps: 5,
      };
    },
    computed: {
      modelSliderPos: {
        set(d) {
          this.$emit('changeSliderPos', d);
        },
        get() {
          return this.currentSliderPosition;
        },
      },
      isPreviousButtonDisable() {
        return !this.isWalkable(-1);
      },
      isNextButtonDisable() {
        return !this.isWalkable();
      },
      isWalkable(deltaStep = 1) {
        return (
          !this.disableOverride &&
          1 <= this.sliderPos + deltaStep &&
          this.sliderPos + deltaStep <= this.sliderLength
        );
      },
    },
    methods: {
      showLabelAlwaysSwitch() {
        this.sliderLabelAlways = !this.sliderLabelAlways;
      },
      disableStepSlider() {
        // TODO
        return this.sliderLength <= 1;
      },
      onSliderChange(pos) {
        this.$emit('onSliderChange', pos);
      },
      onMultipleStepsBack() {
        this.$emit('onStepBack', this.skipSteps);
      },
      onStepBack() {
        this.$emit('onStepBack', 1);
      },
      onStepForward() {
        this.$emit('onStepForward', 1);
      },
      onMultipleStepForward() {
        this.$emit('onStepForward', this.skipSteps);
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
      notAvailableMessage,
    },
  };
</script>
