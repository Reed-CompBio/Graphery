<template>
  <q-header class="q-py-sm q-px-xs" elevated>
    <!--    TODO change the color in dark mode    -->
    <q-toolbar>
      <router-link to="/" class="q-ml-sm">
        <q-img
          alt="Reed Logo"
          class="shrink mr-2"
          contain
          transition="scale-transition"
          width="40px"
          :src="siteLogo"
        >
          <!-- Logo section on the top left corner -->
        </q-img>
      </router-link>

      <!-- TODO Make it on click -->
      <q-toolbar-title style="text-transform: uppercase; font-size: 27px">
        {{ siteName }}
      </q-toolbar-title>

      <div class="gt-sm">
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
            <!-- TODO you may need to use a custom list of lang here -->
            <q-item
              v-for="lang in $i18n.availableLocales"
              :key="lang"
              clickable
              v-close-popup
              @click="changeLocal(lang)"
            >
              <q-item-section avatar>
                <q-icon
                  :name="
                    $i18n.locale === lang
                      ? 'keyboard_arrow_right'
                      : 'fiber_manual_record'
                  "
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="lang-label">{{ lang }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
      <q-btn flat round dense class="lt-md" size="20px">
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
        siteLogo: require('@/assets/images/reed-compbio-logo.png'),
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
</style>
