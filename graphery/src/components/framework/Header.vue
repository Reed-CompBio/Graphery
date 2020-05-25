<template>
  <q-header class="q-py-sm q-px-xs">
    <!--    TODO change the color in dark mode    -->
    <q-toolbar>
      <router-link to="/" class="q-ml-sm">
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
      <q-toolbar-title style="text-transform: uppercase; font-size: 27px">
        {{ siteName }}
      </q-toolbar-title>

      <div class="gt-sm">
        <!-- page buttons -->
        <q-btn
          flat
          rounded
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
          class="q-ml-sm"
          size="18px"
          exact
        >
          {{ button.name }}
        </q-btn>
      </div>
      <q-btn flat round dense class="lt-md" size="20px">
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
        siteName: (state) => state.meta.siteName,
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
