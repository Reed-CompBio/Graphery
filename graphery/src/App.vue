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
  import { LocalStorage } from 'quasar';

  export default Vue.extend({
    name: 'App',

    components: {
      Header: () => import('@/components/framework/Header.vue'),
      Footer: () => import('@/components/framework/Footer.vue'),
      NavigationDrawer: () =>
        import('@/components/framework/NavigationDrawer.vue'),
      Notification: () => import('@/components/framework/Notification.vue'),
    },
    mounted() {
      // this.$q.dark.set(true);
      console.log('empty local storage? ', LocalStorage.isEmpty());
      console.log('local storage: ', LocalStorage.getAll());
      LocalStorage.set('test-key', false);
    },
  });
</script>

<style lang="sass">
  .body--light
    background-color: #f8f8f8
  footer
    a, a:visited
      color: #fff
</style>
