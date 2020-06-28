<template>
  <div id="editor-container">
    <q-bar>
      <q-icon name="mdi-function" />
      <div style="text-transform: uppercase;">{{ routerViewName }}</div>
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
    </q-bar>
    <q-card class="popup-wrapper full-height">
      <router-view class="full-height" :name="routerViewName"></router-view>
      <!-- TODO use child router link instead of tab panel -->
      <!-- TODO use q-fab instead of sticky -->
    </q-card>
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
      <!--      <SwitchTooltip :text="$t('tooltips.showEditorAndMore')"></SwitchTooltip>-->
      <!--      <q-btn round color="primary" icon="mdi-code-json" @click="toggleEditor" />-->
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
        routerViewName: 'editor',
      };
    },
    methods: {
      switchTabView(tabName) {
        this.routerViewName = tabName;
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
