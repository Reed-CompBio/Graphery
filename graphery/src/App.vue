<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <navigation-buttons></navigation-buttons>
    </v-app-bar>

    <v-content>
      <HelloWorld />
    </v-content>
  </v-app>
</template>

<script lang="ts">
  import Vue from 'vue';
  import HelloWorld from './components/HelloWorld.vue';
  import NavigationButtons from '@/components/Frame/NavigationButtons.vue';

  export default Vue.extend({
    name: 'App',

    components: {
      HelloWorld,
      NavigationButtons,
    },

    data: () => ({
      //
    }),
  });
</script>
