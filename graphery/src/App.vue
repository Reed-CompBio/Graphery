<template>
  <q-layout view="hHh lpR fFf">
    <Header></Header>
    <q-ajax-bar color="grey" size="5px"></q-ajax-bar>
    <q-page-container>
      <router-view></router-view>
    </q-page-container>
    <Footer v-if="showFooter"></Footer>
    <NavigationDrawer v-if="$q.screen.lt.md"></NavigationDrawer>
  </q-layout>
</template>

<script>
  import Vue from 'vue';
  import { apiClient } from '@/services/apis';
  import { mapState } from 'vuex';
  import NavigationDrawer from '@/components/framework/NavigationDrawer';
  import Header from '@/components/framework/Header';
  import { QAjaxBar } from 'quasar';

  const showFooterRe = /^(\/tutorial\/|\/graph\/|\/control-panel)/;

  export default Vue.extend({
    name: 'App',
    metaInfo: {
      title: 'Main',
      titleTemplate: '%s | Graphery',
      meta: [{ charset: 'utf-8' }],
    },
    components: {
      Header,
      QAjaxBar,
      NavigationDrawer,
      Footer: () => import('@/components/framework/Footer.vue'),
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
        console.log('GitHub: https://github.com/FlickerSoul/Graphery');
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
    created() {
      this.loadCSRFToken();
    },
    mounted() {
      this.asciiArt();
      this.loadLang();
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
