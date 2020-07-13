<template>
  <q-layout view="hHh lpR fFf">
    <Header></Header>
    <q-ajax-bar size="5px"></q-ajax-bar>
    <q-page-container>
      <router-view></router-view>
    </q-page-container>
    <Footer v-if="showFooter"></Footer>
    <NavigationDrawer></NavigationDrawer>
    <Notification></Notification>
  </q-layout>
</template>

<script lang="ts">
  import Vue from 'vue';

  const showFooterRe = /^(\/tutorial\/|\/graph\/)/;

  export default Vue.extend({
    name: 'App',
    components: {
      Header: () => import('@/components/framework/Header.vue'),
      Footer: () => import('@/components/framework/Footer.vue'),
      NavigationDrawer: () =>
        import('@/components/framework/NavigationDrawer.vue'),
      Notification: () => import('@/components/framework/Notification.vue'),
    },
    computed: {
      showFooter() {
        return !showFooterRe.test(this.$route.fullPath);
      },
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
      console.log('GitHub: https://github.com/poppy-poppy/Graphery');

      // load $q.dark.set is in Header.vue
      // Load language
      // TODO add a preferred language
      this.$i18n.locale = this.$store.state.settings.language;
    },
  });
</script>

<style lang="sass">
  @import "~@/styles/global.sass"
  .body--light
    background-color: #f8f8f8
</style>
