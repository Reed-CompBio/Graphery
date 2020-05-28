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
  import { SettingInfos } from '@/store/states/state';
  import { mapGetters, mapActions } from 'vuex';

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
      ...mapGetters('settings', ['getSettings']),
    },
    methods: {
      ...mapActions('settings', ['storeSettings']),
      initSettings() {
        const settings: { settingVer: SettingInfos } = this.getSettings;
        LocalStorage.set('setting_ver', Object.keys(settings)[0]);
        LocalStorage.set('website_settings', Object.values(settings)[0]);
      },
      loadSettings() {
        this.storeSettings(LocalStorage.getItem('website_settings'));
      },
      settingLoader() {
        if (LocalStorage.has('setting_ver')) {
          this.loadSettings();
        } else {
          this.initSettings();
        }
      },
    },
    mounted() {
      // this.$q.dark.set(true);
      this.settingLoader();
      console.debug('local storage: ', LocalStorage.getAll());
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
