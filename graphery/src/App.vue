<template>
  <q-layout view="hHh lpR fFf">
    <Header></Header>
    <q-ajax-bar color="grey" size="5px"></q-ajax-bar>
    <q-page-container>
      <router-view></router-view>
    </q-page-container>
    <Footer v-if="showFooter"></Footer>
    <NavigationDrawer v-if="$q.screen.lt.md"></NavigationDrawer>
    <Notification></Notification>
  </q-layout>
</template>

<script>
  import Vue from 'vue';
  import { apiClient } from '@/services/apis';
  import { mapState } from 'vuex';

  const showFooterRe = /^(\/tutorial\/|\/graph\/|\/control-panel)/;

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
      ...mapState('settings', ['dark']),
      showFooter() {
        return !showFooterRe.test(this.$route.fullPath);
      },
    },
    methods: {
      asciiArt() {
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
      },
      loadLang() {
        // Load language
        // TODO add a preferred language
        this.$i18n.locale = this.$store.state.settings.language;
      },
      loadCSRFToken() {
        apiClient
          .get('/csrf')
          .then((re) => {
            this.$store.commit('SET_CSRF_TOKEN', re.data.csrfToken);
          })
          .catch((err) => {
            console.error(`Cannot get CSRF token in App. ${err}`);
          });
      },
      loadDarkTheme() {
        this.$q.dark.set(this.dark);
      },
    },
    mounted() {
      this.asciiArt();
      this.loadLang();
      this.loadCSRFToken();
      this.loadDarkTheme();
    },
    watch: {
      dark: function() {
        this.loadDarkTheme();
      },
    },
  });
</script>

<style lang="sass">
  @import "~@/styles/global.sass"
  .body--light
    background-color: #f8f8f8
</style>
