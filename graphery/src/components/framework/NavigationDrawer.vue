<template>
  <v-navigation-drawer
    app
    right
    temporary
    v-model="drawer"
    style="z-index: 9000"
  >
    <v-list rounded>
      <v-card class="mb-4" to="/">
        <v-card-title class="justify-center" style="text-transform: uppercase">
          <v-avatar class="mr-2">
            <img :src="logo" alt="John" />
          </v-avatar>
          Graphery</v-card-title
        >
      </v-card>
      <v-list-item-group>
        <v-list-item
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
          exact
        >
          <v-list-item-icon>
            <v-icon>{{ button.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ button.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
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
