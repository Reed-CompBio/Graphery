<template>
  <v-navigation-drawer app right v-model="drawer">
    <v-list rounded>
      <v-list-item-group>
        <v-list-item
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
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
