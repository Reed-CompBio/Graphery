<template>
  <div id="editor-container">
    <q-bar>
      <q-icon name="mdi-function" />
      <div style="text-transform: uppercase;">{{ tab }}</div>
      <q-space />
      <!-- TODO  get the button actions done -->
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
      <q-btn-group flat class="q-mr-md">
        <q-btn dense icon="mdi-content-copy">
          <SwitchTooltip :text="$t('tooltips.copyCodes')"></SwitchTooltip>
        </q-btn>
        <q-btn dense icon="mdi-content-paste">
          <SwitchTooltip :text="$t('tooltips.pasteCodes')"></SwitchTooltip>
        </q-btn>
      </q-btn-group>
      <q-btn
        dense
        flat
        icon="close"
        @click="closeEditor"
        v-touch-pan.prevent.mouse="null"
      />
    </q-bar>
    <q-card class="popup-wrapper full-height" v-show="editorShow">
      <router-view class="full-height"></router-view>
      <!--      <q-tabs dense inline-label class="tutorial-tabs" v-model="tab">-->
      <!--        <q-tab name="code" icon="mdi-code-braces" label="code" />-->
      <!--        <q-tab name="info" icon="mdi-information-variant" label="info" />-->
      <!--        <q-tab-->
      <!--          name="settings"-->
      <!--          icon="mdi-card-bulleted-settings"-->
      <!--          label="settings"-->
      <!--        />-->
      <!--        <q-tab-->
      <!--          name="shortcuts"-->
      <!--          icon="mdi-format-list-bulleted"-->
      <!--          label="shortcuts"-->
      <!--        >-->
      <!--        </q-tab>-->
      <!--      </q-tabs>-->
      <!--      <q-separator />-->
      <!-- TODO use child router link instead of tab panel -->
      <!-- TODO use q-fab instead of sticky -->
      <!-- -->
      <!--      <q-tab-panels-->
      <!--        animated-->
      <!--        keep-alive-->
      <!--        class="tutorial-tab-panes"-->
      <!--        v-model="tab"-->
      <!--        style="height: 100% !important;"-->
      <!--      >-->
      <!--        <q-tab-panel name="code" class="full-height">-->
      <!--          <Editor :style="editorWrapperStyle"></Editor>-->
      <!--        </q-tab-panel>-->
      <!--        <q-tab-panel name="info">-->
      <!--          &lt;!&ndash; TODO fill in info section &ndash;&gt;-->
      <!--          <div id="info-panel">info</div>-->
      <!--        </q-tab-panel>-->
      <!--        <q-tab-panel name="settings">-->
      <!--          &lt;!&ndash; TODO maybe I don't need this &ndash;&gt;-->
      <!--          <div id="settings-panel">settings</div>-->
      <!--        </q-tab-panel>-->
      <!--        <q-tab-panel name="shortcuts">-->
      <!--          &lt;!&ndash; TODO fill in shortcuts section &ndash;&gt;-->
      <!--          <div id="shortcuts-panel">shortcuts</div>-->
      <!--        </q-tab-panel>-->
      <!--      </q-tab-panels>-->
    </q-card>
    <q-page-sticky
      v-if="$q.screen.gt.xs"
      position="bottom-left"
      :offset="[30, 30]"
    >
      <SwitchTooltip :text="$t('tooltips.showEditorAndMore')"></SwitchTooltip>
      <q-btn round color="primary" icon="mdi-code-json" @click="toggleEditor" />
    </q-page-sticky>
  </div>
</template>

<script>
  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
    },
    data() {
      return {
        editorShow: true,
        tab: 'code',
      };
    },
    methods: {
      toggleEditor() {
        this.editorShow = !this.editorShow;
      },
      closeEditor() {
        this.editorShow = false;
      },
    },
  };
</script>

<style scoped lang="sass">
  .q-tab-panel
    padding: 8px
  #editor-container
    position: absolute
    z-index: auto
    height: 100% !important
    width: 100% !important
</style>
