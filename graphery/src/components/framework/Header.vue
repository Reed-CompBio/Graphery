<template>
  <q-header class="q-py-sm q-px-xs">
    <!--    TODO change the color in dark mode    -->
    <q-toolbar>
      <!-- TODO Make it clickable -->
      <q-toolbar-title id="site-name-section" class="q-ml-lg">
        {{ siteName }}
      </q-toolbar-title>

      <div v-if="$q.screen.gt.sm">
        <!-- page buttons -->
        <q-btn
          flat
          rounded
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
          class="q-ml-sm"
          size="20px"
          exact
        >
          {{ $t(`nav.${button.name}`) }}
        </q-btn>
      </div>
      <div id="language-switcher">
        <LangSelector
          :change-callback="changeLocal"
          :current-lang="$i18n.locale"
        />
      </div>
      <q-btn flat round dense v-if="$q.screen.lt.md" size="20px">
        <q-icon name="mdi-menu" @click="showDrawer" />
      </q-btn>
    </q-toolbar>
  </q-header>
</template>

<script>
  import { siteName, navigationButtons } from '../../store/states/meta';
  import LangSelector from '../ControlPanel/parts/LangSelector';

  export default {
    name: 'Header',
    components: { LangSelector },
    data() {
      return {
        siteName,
        buttons: navigationButtons,
      };
    },
    methods: {
      showDrawer() {
        this.$store.dispatch('changeDrawerState', true);
      },
      changeLocal(lang) {
        this.$i18n.locale = lang;
        this.$store.dispatch('settings/changeLanguage', lang);
      },
    },
  };
</script>

<style lang="sass">
  #site-name-section
    font-family: 'Amiri', serif
    text-transform: uppercase
    font-size: 28px
    padding-top: 5px
</style>
