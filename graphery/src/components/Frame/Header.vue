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
      <!-- Logo section on the top left corner -->
    </v-img>
    <div class="display-1 font-weight-black">Graphery</div>
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
      >
        {{ button.name }}
      </v-btn>
    </div>

    <!-- show burger button when the screen is too samll -->
    <v-app-bar-nav-icon
      class="hidden-md-and-up"
      @click="showDrawer"
    ></v-app-bar-nav-icon>
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
