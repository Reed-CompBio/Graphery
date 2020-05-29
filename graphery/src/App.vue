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
      // draw ascii art
      console.log(
        '%c' +
          ' o-o               o                 \n' +
          'o                  |                 \n' +
          '|  -o o-o  oo o-o  O--o o-o o-o o  o \n' +
          "o   | |   | | |  | |  | |-' |   |  | \n" +
          ' o-o  o   o-o-O-o  o  o o-o o   o--O \n' +
          '              |                    | \n' +
          '              o                 o--o ',
        'color: #A70E16'
      );
      console.log('Welcome to Graphery, a graph tutorial website');
      console.log('GitHub: https://github.com/FlickerSoul/Graphery');

      // load $q.dark.set is in Header.vue
      // Load language
      this.$i18n.locale = this.$store.state.settings.language;
    },
    // TODO add a version check to local settings
  });
</script>

<style lang="sass">
  .body--light
    background-color: #f8f8f8
  footer
    a, a:visited
      color: #fff
</style>
