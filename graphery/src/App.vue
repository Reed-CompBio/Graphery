<template>
  <q-layout view="hHh lpR fFf">
    <Header></Header>
    <q-page-container>
      <router-view></router-view>
    </q-page-container>
    <Footer v-if="this.$route.name !== 'Tutorial'"></Footer>
    <NavigationDrawer></NavigationDrawer>
    <Notification></Notification>
  </q-layout>
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

<style>
  .fill-height {
    height: 100%;
  }
</style>
