<template>
  <v-app-bar app>
    <!-- logo width is 40 pe -->
    <v-img
      alt="Reed Logo"
      class="shrink mr-2"
      contain
      transition="scale-transition"
      width="40"
      :src="siteLogo"
    >
      <!-- src="data:image/png;base64,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" -->
      <!-- Logo section on the top left corner -->
    </v-img>
    <div
      class="display-1 font-weight-black"
      style="font-family: 'Libre Baskerville', serif!important ; /* font-size: 1.8rem !important */"
    >Graphery</div>
    <!-- adding spacing to the elements -->
    <v-spacer></v-spacer>
    <!-- navigation buttons when the screen is bigger than  md-->
    <div class="hidden-sm-and-down">
      <!-- TODO bug:the home button is always active -->
      <!-- page buttons -->
      <v-btn
        class="ma-1"
        rounded
        text
        v-for="button in buttons"
        :key="button.name"
        :to="button.name == 'Home' ? '/' : { name: button.name }"
      >{{ button.name }}</v-btn>
    </div>

    <!-- show burger button when the screen is too samll -->
    <v-app-bar-nav-icon class="hidden-md-and-up" @click="showDrawer"></v-app-bar-nav-icon>
  </v-app-bar>
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
