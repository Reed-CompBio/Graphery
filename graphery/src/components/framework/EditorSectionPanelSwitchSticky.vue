<template>
  <q-page-sticky
    v-if="$q.screen.gt.xs"
    position="bottom-left"
    :offset="[30, 30]"
    style="z-index: 5"
  >
    <q-fab direction="up" color="primary" icon="more_horiz" padding="10px">
      <q-fab-action
        color="accent"
        icon="mdi-code-json"
        padding="10px"
        @click.prevent="switchTabView('editor')"
      >
        <SwitchTooltip
          :text="$t('tooltips.editor')"
          self="center left"
          anchor="center right"
        />
      </q-fab-action>
      <q-fab-action
        color="positive"
        icon="info"
        padding="10px"
        @click.prevent="switchTabView('graph-info')"
      >
        <SwitchTooltip
          :text="$t('tooltips.graphInfo')"
          self="center left"
          anchor="center right"
        />
      </q-fab-action>
      <q-fab-action
        color="orange"
        icon="help"
        padding="10px"
        @click.prevent="switchTabView('how-to')"
      >
        <SwitchTooltip
          :text="$t('tooltips.howTo')"
          self="center left"
          anchor="center right"
        />
      </q-fab-action>
      <!-- TODO added graph info and how to use editor here -->
      <template v-slot:tooltip>
        <SwitchTooltip
          :text="$t('tooltips.showEditorAndMore')"
          self="center left"
          anchor="center right"
        ></SwitchTooltip>
      </template>
    </q-fab>
  </q-page-sticky>
</template>

<script>
  export default {
    components: {
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip'),
    },
    methods: {
      switchTabView(tabName) {
        this.$emit('switchTab', tabName);
      },
    },
  };
</script>
