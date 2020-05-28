<template>
  <MaterialPage>
    <div>
      <div>
        <h3 class="shorter-h">
          Settings
        </h3>
      </div>
      <section>
        <q-card class="q-pa-md q-my-lg">
          <q-card-section>
            <h4 class="q-my-sm">
              Colors
            </h4>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <div class="q-pl-md">
              <q-toggle
                left-label
                size="xl"
                label="Dark Mode"
                v-model="darkMode"
                color="black"
                checked-icon="mdi-moon-waxing-crescent"
                unchecked-icon="mdi-white-balance-sunny"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                label="Graph Background Dark"
                v-model="graphBackgroundDark"
                color="grey"
                checked-icon="mdi-decagram"
                unchecked-icon="mdi-decagram-outline"
              />
            </div>
          </q-card-section>
        </q-card>
        <q-card class="q-pa-md">
          <q-card-section>
            <h4 class="q-my-sm">
              Graph Render
            </h4>
            <span>(Turn on to gain performance)</span>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <div class="q-pl-md">
              <q-toggle
                left-label
                size="xl"
                label="Hide Edges When Rendering"
                v-model="renderingHideEdge"
                color="green"
                checked-icon="mdi-eye-off"
                unchecked-icon="mdi-eye"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                label="Render Viewport Only"
                v-model="onlyRenderViewport"
                color="orange"
                checked-icon="mdi-fullscreen-exit"
                unchecked-icon="mdi-fullscreen"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                label="Motion Blur Enabled"
                v-model="enableMotionBlur"
                color="blue"
                checked-icon="mdi-run-fast"
                unchecked-icon="mdi-run"
              />
            </div>
            <q-item>
              <q-item-section>
                <span>Motion Sensitivity Level</span>
              </q-item-section>
              <q-item-section>
                <q-slider
                  label
                  label-always
                  snap
                  v-model="graphMotionSensitivity"
                  color="teal"
                  :min="0.5"
                  :step="0.1"
                  :max="2"
                />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
                <span>Tutorial Page Default Split Pos (%)</span>
              </q-item-section>
              <q-item-section>
                <q-slider
                  label
                  label-always
                  snap
                  v-model="tutorialSplitPos"
                  color="deep-orange"
                  :min="10"
                  :step="1"
                  :max="90"
                />
              </q-item-section>
            </q-item>
          </q-card-section>
        </q-card>
        <q-card class="q-pa-md q-my-lg">
          <q-card-section>
            <h4 class="q-my-sm">
              Editor Settings
            </h4>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <div class="q-pl-md">
              <q-toggle
                left-label
                size="xl"
                label="Soft Tab"
                v-model="usingSoftTab"
                color="green-4"
                checked-icon="mdi-keyboard-space"
                unchecked-icon="mdi-keyboard-tab"
              />
              <br />
              <q-toggle
                left-label
                size="xl"
                label="Line Wrap"
                v-model="usingLineWrap"
                color="orange-4"
                checked-icon="mdi-wrap"
                unchecked-icon="mdi-wrap-disabled"
              />
            </div>
            <q-item>
              <q-item-section>
                <span>Tab Space Number</span>
              </q-item-section>
              <q-item-section>
                <q-slider
                  label
                  label-always
                  snap
                  v-model="softTabNum"
                  color="light-blue"
                  :min="2"
                  :step="1"
                  :max="6"
                />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
                <span>Tab Space Number</span>
              </q-item-section>
              <q-item-section>
                <q-slider
                  label
                  label-always
                  snap
                  v-model="fontSize"
                  color="amber"
                  :min="8"
                  :step="1"
                  :max="20"
                />
              </q-item-section>
            </q-item>
          </q-card-section>
        </q-card>
      </section>
    </div>
  </MaterialPage>
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
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
        'wrap',
      ]),
      darkMode: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.dark;
        },
      },
      graphBackgroundDark: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.graphDark;
        },
      },
      renderingHideEdge: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.hideEdgeWhenRendering;
        },
      },
      onlyRenderViewport: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.renderViewportOnly;
        },
      },
      enableMotionBlur: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.motionBlurEnabled;
        },
      },
      tutorialSplitPos: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.graphSplitPos;
        },
      },
      graphMotionSensitivity: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.motionSensitivityLevel;
        },
      },
      usingSoftTab: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.softTab;
        },
      },
      usingLineWrap: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.wrap;
        },
      },
      softTabNum: {
        set(d) {
          console.log(d);
        },
        get() {
          return this.tabNum;
        },
      },
      // TODO font size is not settled
    },
  };
</script>
