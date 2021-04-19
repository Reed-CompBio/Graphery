<template>
  <div :style="panelStyle">
    <!-- Left drawer-->
    <q-layout view="hHh Lpr lff" container class="full-height">
      <q-drawer
        v-model="showDrawer"
        show-if-above
        :width="300"
        :breakpoint="700"
        elevated
      >
        <q-list>
          <q-card class="q-py-md">
            <q-card-section>
              <q-item>
                <q-item-section>
                  <div class="text-h5">
                    Control Panel
                  </div>
                </q-item-section>
              </q-item>
            </q-card-section>
          </q-card>
          <DrawerListItem
            :destination="{ name: 'Control Panel' }"
            title="Main"
          />
          <DrawerListItem
            :destination="{ name: 'Uploads List' }"
            title="Uploads"
          />
          <DrawerListItem
            :destination="{ name: 'Category List' }"
            title="Categories"
          />
          <DrawerListItem
            :destination="{ name: 'Tutorial Anchor List' }"
            title="Tutorial Anchors"
          />
          <DrawerListItem
            :destination="{ name: 'Tutorial Content List' }"
            title="Tutorial Content"
          />
          <DrawerListItem
            :destination="{ name: 'Graph List' }"
            title="Graphs"
          />
          <DrawerListItem
            :destination="{ name: 'Graph Info List' }"
            title="Graph Info"
          />
          <DrawerListItem :destination="{ name: 'Code List' }" title="Code" />
        </q-list>
      </q-drawer>

      <q-page-container>
        <q-page>
          <!--          <keep-alive :exclude="/.*Creation.*/">-->
          <router-view></router-view>
          <!--          </keep-alive>-->
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
  <!-- TODO put a full screen undismissiable dialog telling user they should not use mobile to access this page -->
</template>

<script>
  import { headerSize } from '../store/states/meta';

  export default {
    components: {
      DrawerListItem: () =>
        import('@/components/ControlPanel/parts/DrawerListItem.vue'),
    },
    data() {
      return {
        showDrawer: true,
        tabName: 'main',
      };
    },
    computed: {
      panelStyle() {
        return {
          height: `calc(100vh - ${headerSize}px)`,
        };
      },
    },
  };
</script>
