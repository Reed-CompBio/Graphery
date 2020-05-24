<template>
  <q-drawer
    overlay
    behavior="mobile"
    side="right"
    :persistent="false"
    v-model="drawer"
    style="z-index: 9000"
  >
    <q-list>
      <q-card class="q-py-lg" to="/">
        <q-card-section>
          <q-item>
            <q-item-section avatar>
              <q-avatar class="mr-2">
                <img :src="logo" alt="Reed CompBio Logo" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <div class="text-h4" style="text-transform: uppercase">
                Graphery
              </div>
            </q-item-section>
          </q-item>
        </q-card-section>
      </q-card>
      <div class="q-pt-md q-pl-xl">
        <q-item
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
          exact
        >
          <q-item-section avatar>
            <q-icon :name="button.icon"></q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label header style="text-transform: uppercase">{{
              button.name
            }}</q-item-label>
          </q-item-section>
        </q-item>
      </div>
    </q-list>
  </q-drawer>
</template>

<script>
  import { mapState } from 'vuex';
  export default {
    computed: {
      ...mapState({
        logo: (state) => state.meta.siteLogo,
        buttons: (state) => state.meta.navigationButtons,
        drawerState: (state) => state.drawer,
      }),
      // temporary workaround
      drawer: {
        set(d) {
          this.$store.dispatch('changeDrawerState', d);
        },
        get() {
          return this.drawerState;
        },
      },
    },
  };
</script>
