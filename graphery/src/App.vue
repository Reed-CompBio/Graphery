<template>
  <v-app>
    <Header></Header>
    <v-content>
      <router-view></router-view>
    </v-content>
    <Footer></Footer>
    <navigation-drawer></navigation-drawer>
  </v-app>
</template>

<script lang="ts">
  import Vue from 'vue';
  import Header from '@/components/frame/Header.vue';
  import Footer from '@/components/frame/Footer.vue';
  import NavigationDrawer from '@/components/frame/NavigationDrawer.vue';

  export default Vue.extend({
    name: 'App',

    components: {
      Header,
      Footer,
      NavigationDrawer,
    },

    data: () => ({
      //
    }),
  });
</script>
