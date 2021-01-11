<template>
  <!-- the content is still very message -->
  <MaterialPage>
    <div>
      <div id="header-section">
        <h3 class="material-page-shorter-h3">
          {{ $t('nav.Settings') }}
        </h3>
      </div>
      <div id="content-section">
        <SettingDisplayCard :title="$t('settings.Display')">
          <template v-slot:toggles>
            <SettingUnit
              :name="$t('settings.darkMode') + '  (Just DON\'T Use it )'"
            >
              <q-toggle
                left-label
                size="xl"
                v-model="setDarkMode"
                color="black"
                checked-icon="mdi-moon-waxing-crescent"
                unchecked-icon="mdi-white-balance-sunny"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.graphBackgroundDark')">
              <q-toggle
                left-label
                size="xl"
                v-model="setGraphBackgroundDark"
                color="grey"
                checked-icon="mdi-decagram"
                unchecked-icon="mdi-decagram-outline"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.showTooltips')">
              <q-toggle
                left-label
                size="xl"
                v-model="setTooltips"
                color="green-4"
                checked-icon="mdi-comment-check"
                unchecked-icon="mdi-comment-remove"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.Show Graph Abstract')">
              <q-toggle
                left-label
                size="xl"
                v-model="setGraphAbstractPopupShow"
                checked-icon="mdi-layers"
                unchecked-icon="mdi-layers-off"
              />
            </SettingUnit>
          </template>
          <template v-slot:sliders>
            <SettingUnit :name="$t('settings.cardsDisplayedNum')">
              <q-slider
                label
                label-always
                markers
                snap
                v-model="setPageDisplayNum"
                color="amber"
                :min="1"
                :step="1"
                :max="10"
              />
            </SettingUnit>
          </template>
        </SettingDisplayCard>

        <SettingDisplayCard :title="$t('settings.graphRender')">
          <template v-slot:toggles>
            <p>({{ $t('settings.performanceTip') }})</p>
            <SettingUnit :name="$t('settings.hideEdgesWhenRendering')">
              <q-toggle
                left-label
                size="xl"
                v-model="setHideEdgeWhenRendering"
                color="green"
                checked-icon="mdi-eye-off"
                unchecked-icon="mdi-eye"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.renderViewportOnly')">
              <q-toggle
                left-label
                size="xl"
                v-model="setRenderViewportOnly"
                color="orange"
                checked-icon="mdi-fullscreen-exit"
                unchecked-icon="mdi-fullscreen"
              />
            </SettingUnit>

            <SettingUnit :name="$t('settings.motionBlurEnabled')">
              <q-toggle
                left-label
                size="xl"
                v-model="setMotionBlurEnabled"
                color="blue"
                checked-icon="mdi-run-fast"
                unchecked-icon="mdi-run"
              />
            </SettingUnit>
          </template>
          <template v-slot:sliders>
            <SettingUnit :name="$t('settings.motionSensitivityLevel')">
              <q-slider
                label
                label-always
                snap
                v-model="setMotionSensitivityLevel"
                color="teal"
                :min="0.5"
                :step="0.1"
                :max="2"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.splitPos')">
              <q-slider
                label
                label-always
                snap
                v-model="setGraphSplitPos"
                color="deep-orange"
                :min="10"
                :step="0.1"
                :max="90"
              />
            </SettingUnit>
          </template>
        </SettingDisplayCard>

        <SettingDisplayCard :title="$t('settings.editorSettings')">
          <template v-slot:toggles>
            <SettingUnit :name="$t('settings.enableEditing')">
              <q-toggle
                left-label
                size="xl"
                v-model="setEnableEditing"
                color="accent"
                checked-icon="lock_open"
                unchecked-icon="lock"
              ></q-toggle>
            </SettingUnit>
            <SettingUnit :name="$t('settings.softTab')">
              <q-toggle
                left-label
                size="xl"
                v-model="setSoftTab"
                color="green-4"
                checked-icon="mdi-keyboard-space"
                unchecked-icon="mdi-keyboard-tab"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.lineWrap')">
              <q-toggle
                left-label
                size="xl"
                v-model="setCodeWrap"
                color="orange-4"
                checked-icon="mdi-wrap"
                unchecked-icon="mdi-wrap-disabled"
              />
            </SettingUnit>
          </template>
          <template v-slot:sliders>
            <SettingUnit :name="$t('settings.tabNum')">
              <q-slider
                label
                label-always
                markers
                snap
                v-model="setTabNum"
                color="light-blue"
                :min="2"
                :step="1"
                :max="6"
              />
            </SettingUnit>
            <SettingUnit :name="$t('settings.fontSize')">
              <q-slider
                label
                label-always
                markers
                snap
                v-model="setFontSize"
                color="amber"
                :min="8"
                :step="1"
                :max="20"
              />
            </SettingUnit>
          </template>
        </SettingDisplayCard>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  import MaterialPage from '@/components/framework/MaterialPage.vue';
  import SettingDisplayCard from '@/components/settings/SettingDisplayCard';
  import SettingUnit from '@/components/settings/SettingUnit';
  export default {
    metaInfo() {
      const titleText = this.$t('nav.Settings');
      return { title: titleText };
    },
    components: {
      MaterialPage,
      SettingDisplayCard,
      SettingUnit,
    },
    computed: {
      ...mapState('settings', [
        'dark',
        'graphDark',
        'graphSplitPos',
        'hideEdgeWhenRendering',
        'renderViewportOnly',
        'motionBlurEnabled',
        'motionSensitivityLevel',
        'enableEditing',
        'tabNum',
        'softTab',
        'fontSize',
        'codeWrap',
        'pageDisplayNum',
        'tooltips',
        'graphAbstractPopupShow',
      ]),
      setDarkMode: {
        set(d) {
          this.changeDark(d);
        },
        get() {
          return this.dark;
        },
      },
      setGraphBackgroundDark: {
        set(d) {
          this.changeGraphDark(d);
        },
        get() {
          return this.graphDark;
        },
      },
      setHideEdgeWhenRendering: {
        set(d) {
          this.changeHideEdgeWhenRendering(d);
        },
        get() {
          return this.hideEdgeWhenRendering;
        },
      },
      setRenderViewportOnly: {
        set(d) {
          this.changeRenderViewportOnly(d);
        },
        get() {
          return this.renderViewportOnly;
        },
      },
      setMotionBlurEnabled: {
        set(d) {
          this.changeMotionBlurEnabled(d);
        },
        get() {
          return this.motionBlurEnabled;
        },
      },
      setMotionSensitivityLevel: {
        set(d) {
          this.changeMotionSensitivityLevel(d);
        },
        get() {
          return this.motionSensitivityLevel;
        },
      },
      setGraphSplitPos: {
        set(d) {
          this.changeGraphSplitPos(d);
        },
        get() {
          return this.graphSplitPos;
        },
      },
      setEnableEditing: {
        set(d) {
          this.changeEnableEditing(d);
        },
        get() {
          return this.enableEditing;
        },
      },
      setTabNum: {
        set(d) {
          this.changeTabNum(d);
        },
        get() {
          return this.tabNum;
        },
      },
      setSoftTab: {
        set(d) {
          this.changeSoftTab(d);
        },
        get() {
          return this.softTab;
        },
      },
      setFontSize: {
        set(d) {
          this.changeFontSize(d);
        },
        get() {
          return this.fontSize;
        },
      },
      setCodeWrap: {
        set(d) {
          this.changeCodeWrap(d);
        },
        get() {
          return this.codeWrap;
        },
      },
      setPageDisplayNum: {
        set(d) {
          this.changePageDisplayNum(d);
        },
        get() {
          return this.pageDisplayNum;
        },
      },
      setTooltips: {
        set(d) {
          this.changeTooltips(d);
        },
        get() {
          return this.tooltips;
        },
      },
      setGraphAbstractPopupShow: {
        set(d) {
          this.changeGraphAbstractPopupShow(d);
        },
        get() {
          return this.graphAbstractPopupShow;
        },
      },
    },
    methods: {
      ...mapActions('settings', [
        'changeDark',
        'changeGraphDark',
        'changeHideEdgeWhenRendering',
        'changeRenderViewportOnly',
        'changeMotionBlurEnabled',
        'changeMotionSensitivityLevel',
        'changeGraphSplitPos',
        'changeEnableEditing',
        'changeTabNum',
        'changeSoftTab',
        'changeFontSize',
        'changeCodeWrap',
        'changePageDisplayNum',
        'changeTooltips',
        'changeGraphAbstractPopupShow',
      ]),
    },
  };
</script>
