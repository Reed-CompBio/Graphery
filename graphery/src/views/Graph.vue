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
        <div>
          <q-bar class="graph-menu-bar">
            <div class="graph-menu-wrapper">
              <q-select
                class="graph-selector"
                :options="getCodeList"
                v-model="graphChoice"
                label="Graph"
                :multiple="false"
                dropdown-icon="mdi-menu-down"
                :loading="graphsEmpty"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      No results
                    </q-item-section>
                  </q-item>
                </template>
                <template v-slot:prepend>
                  <q-icon name="mdi-graphql"></q-icon>
                </template>
              </q-select>
            </div>
            <div class="menu-button-group-wrapper">
              <q-btn-group rounded class="menu-button-group q-mx-auto">
                <q-btn-dropdown>
                  <template v-slot:label>
                    <q-icon name="mdi-share-variant" />
                    <SwitchTooltip :text="$t('tooltips.Share')"></SwitchTooltip>
                  </template>
                  <q-list>
                    <!-- share graph json -->
                    <q-item clickable v-close-popup @click="shareGraphJson">
                      <q-item-section avatar>
                        <q-avatar icon="mdi-code-json" />
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>Share Json</q-item-label>
                        <q-item-label caption>
                          Copy the json of this graph
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                    <!-- share graph screen shot -->
                    <q-item
                      clickable
                      v-close-popup
                      @click="shareGraphScreenshot"
                    >
                      <q-item-section avatar>
                        <q-avatar icon="photo" />
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>Share Screenshot</q-item-label>
                        <q-item-label caption>
                          Copy the screenshot of this graph
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-btn-dropdown>
              </q-btn-group>
            </div>
          </q-bar>
          <EditorWrapper style="max-height: calc(100% - 56px);"></EditorWrapper>
        </div>
      </template>
    </q-splitter>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import { headerSize } from '../store/states/meta';

  export default {
    props: ['url'],
    components: {
      EditorWrapper: () => import('@/components/tutorial/EditorWrapper.vue'),
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
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
