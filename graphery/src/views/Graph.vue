<template>
  <div style="overflow: hidden; ">
    <q-splitter
      v-if="$q.screen.gt.xs"
      v-model="splitPos"
      :style="splitterStyle"
      :horizontal="$q.screen.lt.md"
      separator-class="bg-light-blue"
      separator-style="width: 4px"
    >
      <template v-slot:before>
        <CytoscapeWrapper ref="cytoscapeWrapper"></CytoscapeWrapper>
      </template>
      <template v-slot:separator>
        <q-avatar
          color="primary"
          text-color="white"
          size="32px"
          icon="mdi-drag"
        />
      </template>
      <template v-slot:after>
        <Editor :height="100"></Editor>
      </template>
    </q-splitter>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import { headerSize } from '../store/states/meta';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
      Editor: () => import('@/components/tutorial/Editor.vue'),
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
      splitPos: {
        set(d) {
          this.$store.dispatch(
            'settings/changeGraphSplitPos',
            Math.round(d * 10) / 10
          );
        },
        get() {
          return this.graphSplitPos;
        },
      },
      splitterStyle() {
        return {
          height: `calc(100vh - ${headerSize}px)`,
        };
      },
    },
  };
</script>
