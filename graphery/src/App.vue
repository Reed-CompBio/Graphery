<template>
  <v-app>
    <Header></Header>
    <v-content>
      <router-view></router-view>
    </v-content>
    <Footer v-if="this.$route.name != 'Tutorial'"></Footer>
    <navigation-drawer></navigation-drawer>
    <Notification></Notification>
  </v-app>
</template>

<script lang="ts">
  import Vue from 'vue';
  import Header from '@/components/framework/Header.vue';
  import Footer from '@/components/framework/Footer.vue';
  import NavigationDrawer from '@/components/framework/NavigationDrawer.vue';
  import Notification from '@/components/framework/Notification.vue';

  export default Vue.extend({
    name: 'App',

    components: {
      Header,
      Footer,
      NavigationDrawer,
      Notification,
    },
  });
</script>
