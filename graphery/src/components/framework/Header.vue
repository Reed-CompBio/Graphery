<template>
  <q-header class="q-py-sm q-px-xs">
    <!--    TODO change the color in dark mode    -->
    <q-toolbar>
      <!-- TODO Make it clickable -->
      <q-toolbar-title
        id="site-name-section"
        class="q-ml-lg"
        style="text-transform: uppercase; font-size: 30px"
      >
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
          size="18px"
          exact
        >
          {{ $t(`nav.${button.name}`) }}
        </q-btn>
      </div>
      <div id="language-switcher">
        <q-btn-dropdown flat dense icon="mdi-translate">
          <q-list>
            <q-item
              v-for="lang in $i18n.availableLocales"
              :key="lang"
              clickable
              v-close-popup
              @click="changeLocal(lang)"
            >
              <q-item-section thumbnail>
                <q-icon
                  v-if="$i18n.locale === lang"
                  name="keyboard_arrow_right"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="lang-label">{{ lang }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
      <q-btn flat round dense v-if="$q.screen.lt.md" size="20px">
        <q-icon name="mdi-menu" @click="showDrawer" />
      </q-btn>
    </q-toolbar>
  </q-header>
</template>

<script>
  import { siteName, navigationButtons } from '../../store/states/meta';
  import { mapState } from 'vuex';

  export default {
    name: 'Header',
    data() {
      return {
        siteName,
        buttons: navigationButtons,
      };
    },
    computed: {
      ...mapState('settings', ['dark']),
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
    watch: {
      dark: function() {
        this.$q.dark.set(this.dark);
      },
    },
    mounted() {
      this.$q.dark.set(this.dark);
    },
  };
</script>

<style lang="sass">
  .lang-label
    text-align: center
    text-transform: uppercase
    font-weight: bold
  #site-name-section
    font-family: 'Amiri', serif
</style>
