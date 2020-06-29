<template>
  <div id="editor-container">
    <q-bar>
      <q-icon name="mdi-function" />
      <div style="text-transform: uppercase;">{{ routerViewName }}</div>
      <q-space />
      <!-- TODO a bug here, can't display the pin above the slider -->
      <q-slider
        id="stepper-slider"
        v-model="sliderPos"
        :min="1"
        label
        :max="sliderLength"
        :step="1"
        snap
        dense
        style="width: 45%;"
        label-always
        :disable="disableStepSlider"
      ></q-slider>
      <!-- TODO  get the button actions done -->
      <!-- stepper button group -->
      <q-btn-group flat class="q-mr-md">
        <!--        <div>-->
        <q-btn flat dense round icon="mdi-skip-backward"></q-btn>
        <q-btn flat dense round icon="mdi-skip-previous"></q-btn>
        <!--        </div>-->
        <q-btn flat dense round :icon="playPauseButton"></q-btn>
        <!--        <div>-->
        <q-btn flat dense round icon="mdi-skip-next"></q-btn>
        <q-btn flat dense round icon="mdi-skip-forward"></q-btn>
        <!-- TODO auto play -->
        <!--        </div>-->
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
          <q-icon name="mdi-play" />
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
    <div class="row" style="height: calc(100% - 32px)">
      <div class="col full-height">
        <q-card class="popup-wrapper full-height">
          <router-view class="full-height" :name="routerViewName"></router-view>
          <!-- TODO use child router link instead of tab panel -->
          <!-- TODO use q-fab instead of sticky -->
        </q-card>
      </div>
      <div class="col-2">
        <CodeController></CodeController>
      </div>
    </div>
    <q-page-sticky
      v-if="$q.screen.gt.xs"
      position="bottom-left"
      :offset="[30, 30]"
    >
      <q-fab direction="up" color="primary" icon="more_horiz">
        <q-fab-action
          color="secondary"
          icon="mdi-code-json"
          @click.prevent="switchTabView('editor')"
        />
        <q-fab-action
          color="skyblue"
          icon="block"
          @click.prevent="switchTabView('block')"
        />
      </q-fab>
      <!-- TODO change the translation -->
      <SwitchTooltip :text="$t('tooltips.showEditorAndMore')"></SwitchTooltip>
      <!--      <q-btn round color="primary" icon="mdi-code-json" @click="toggleEditor" />-->
    </q-page-sticky>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';

  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
      CodeController: () => import('@/components/tutorial/CodeController.vue'),
    },
    data() {
      return {
        routerViewName: 'editor',
        isPlaying: false,
        sliderPos: 1,
      };
    },
    computed: {
      ...mapGetters('tutorials', ['resultJsonEmpty', 'variableObjEmpty']),

      playPauseButton() {
        if (this.isPlaying) {
          return 'mdi-pause';
        } else {
          return 'mdi-play';
        }
      },
      resultObject() {
        if (this.resultJsonEmpty) {
          return [];
        }
        return JSON.parse(this.resultJson);
      },
      sliderLength() {
        if (this.resultObject) {
          return this.resultObject.length + 1;
        }
        return 1;
      },
      disableStepSlider() {
        return this.sliderLength === 1;
      },
    },
    methods: {
      switchTabView(tabName) {
        this.routerViewName = tabName;
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
