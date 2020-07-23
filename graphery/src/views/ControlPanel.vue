<template>
  <div style="height: calc(100vh - 66px);">
    <!-- Left drawer-->
    <q-layout view="hHh Lpr lff" container class="full-height">
      <q-drawer
        :v-model="true"
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
          <q-item clickable :to="{ name: 'Control Panel' }">
            <q-card-section>
              Main
            </q-card-section>
          </q-item>
          <q-item clickable :to="{ name: 'Category List' }">
            <q-card-section>
              Categories
            </q-card-section>
          </q-item>
          <q-item clickable :to="{ name: 'Tutorial Anchor List' }">
            <q-card-section>
              Tutorial Anchors
            </q-card-section>
          </q-item>
          <q-item clickable :to="{ name: 'Tutorial Content List' }">
            <q-card-section>
              Tutorial Content
            </q-card-section>
          </q-item>
          <q-item clickable :to="{ name: 'Graph List' }">
            <q-card-section>
              Graphs
            </q-card-section>
          </q-item>
        </q-list>
      </q-drawer>

      <q-page-container>
        <q-page>
          <keep-alive>
            <router-view></router-view>
          </keep-alive>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
  <!-- TODO put a full screen undismissiable dialog telling user they should not use mobile to access this page -->
</template>

<script>
  export default {
    data() {
      return {
        showDrawer: true,
        tabName: 'main',
      };
    },
  };
</script>

<style lang="sass">
  .custom-table
    thead tr:first-child th:first-child
      /* bg color is important for th; just specify one */
      background-color: #fff

    td:first-child
      background-color: #f5f5dc

    th
      font-size: 16px

    th:first-child,
    td:first-child
      position: sticky
      left: 0
      z-index: 5
</style>
