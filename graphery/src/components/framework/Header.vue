<template>
  <q-header height-hint="60px" class="q-py-sm q-px-xs">
    <q-toolbar style="z-index: 8000">
      <router-link to="/">
        <q-img
          alt="Reed Logo"
          class="shrink mr-2"
          contain
          transition="scale-transition"
          width="40px"
          :src="siteLogo"
        >
          <!-- Logo section on the top left corner -->
        </q-img>
      </router-link>

      <!--    Make it on click -->
      <q-toolbar-title style="text-transform: uppercase;" to="/">
        Graphery
      </q-toolbar-title>

      <div class="gt-sm">
        <!-- page buttons -->
        <q-btn
          flat
          size="md"
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
          :label="button.name"
          exact
        >
        </q-btn>
      </div>
      <q-btn flat round dense class="lt-md">
        <q-icon name="mdi-menu" @click="showDrawer" />
      </q-btn>
    </q-toolbar>
  </q-header>
</template>

<script>
  import { mapState } from 'vuex';

  export default {
    name: 'Header',
    computed: {
      ...mapState({
        siteLogo: (state) => state.meta.siteLogo,
        buttons: (state) => state.meta.navigationButtons,
      }),
    },
    methods: {
      showDrawer() {
        this.$store.dispatch('changeDrawerState', true);
      },
    },
  };
</script>
