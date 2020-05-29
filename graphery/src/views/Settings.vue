<template>
  <!-- the content is still very message -->
  <MaterialPage>
    <div>
      <div id="header-section">
        <h3 class="shorter-h">
          {{ $t('nav.Settings') }}
        </h3>
      </div>
      <div id="content-section">
        <section class="q-my-lg">
          <SettingDisplayCard :title="$t('settings.Display')">
            <template v-slot:toggles>
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.darkMode')"
                v-model="setDarkMode"
                color="black"
                checked-icon="mdi-moon-waxing-crescent"
                unchecked-icon="mdi-white-balance-sunny"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.graphBackgroundDark')"
                v-model="setGraphBackgroundDark"
                color="grey"
                checked-icon="mdi-decagram"
                unchecked-icon="mdi-decagram-outline"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.showTooltips')"
                v-model="setTooltips"
                color="green-4"
                checked-icon="mdi-comment-check"
                unchecked-icon="mdi-comment-remove"
              />
            </template>
            <template v-slot:sliders>
              <q-item>
                <q-item-section>
                  <span>{{ $t('settings.cardsDisplayedNum') }}</span>
                </q-item-section>
                <q-item-section>
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
                </q-item-section>
              </q-item>
            </template>
          </SettingDisplayCard>
        </section>
        <section class="q-my-lg">
          <SettingDisplayCard :title="$t('settings.graphRender')">
            <template v-slot:toggles>
              <p>({{ $t('settings.performanceTip') }})</p>
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.hideEdgesWhenRendering')"
                v-model="setHideEdgeWhenRendering"
                color="green"
                checked-icon="mdi-eye-off"
                unchecked-icon="mdi-eye"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.renderViewportOnly')"
                v-model="setRenderViewportOnly"
                color="orange"
                checked-icon="mdi-fullscreen-exit"
                unchecked-icon="mdi-fullscreen"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.motionBlurEnabled')"
                v-model="setMotionBlurEnabled"
                color="blue"
                checked-icon="mdi-run-fast"
                unchecked-icon="mdi-run"
              />
            </template>
            <template v-slot:sliders>
              <q-item>
                <q-item-section>
                  <span>{{ $t('settings.motionSensitivityLevel') }}</span>
                </q-item-section>
                <q-item-section>
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
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <span>{{ $t('settings.splitPos') }} (%)</span>
                </q-item-section>
                <q-item-section>
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
                </q-item-section>
              </q-item>
            </template>
          </SettingDisplayCard>
        </section>
        <section class=" q-my-lg">
          <SettingDisplayCard :title="$t('settings.editorSettings')">
            <template v-slot:toggles>
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.softTab')"
                v-model="setSoftTab"
                color="green-4"
                checked-icon="mdi-keyboard-space"
                unchecked-icon="mdi-keyboard-tab"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                :label="$t('settings.lineWrap')"
                v-model="setCodeWrap"
                color="orange-4"
                checked-icon="mdi-wrap"
                unchecked-icon="mdi-wrap-disabled"
              />
            </template>
            <template v-slot:sliders>
              <q-item>
                <q-item-section>
                  <span>{{ $t('settings.tabNum') }}</span>
                </q-item-section>
                <q-item-section>
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
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <span>{{ $t('settings.fontSize') }} (px) </span>
                </q-item-section>
                <q-item-section>
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
                </q-item-section>
              </q-item>
            </template>
          </SettingDisplayCard>
        </section>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      SettingDisplayCard: () =>
        import('@/components/settings/SettingDisplayCard.vue'),
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
        'tabNum',
        'softTab',
        'fontSize',
        'codeWrap',
        'pageDisplayNum',
        'tooltips',
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
        'changeTabNum',
        'changeSoftTab',
        'changeFontSize',
        'changeCodeWrap',
        'changePageDisplayNum',
        'changeTooltips',
      ]),
    },
  };
</script>
