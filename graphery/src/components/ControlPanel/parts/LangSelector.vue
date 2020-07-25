<template>
  <q-btn-dropdown
    flat
    dense
    icon="mdi-translate"
    :label="showHeader ? currentLang : null"
  >
    <q-list>
      <q-item
        v-for="lang in $i18n.availableLocales"
        :key="lang"
        clickable
        v-close-popup
        @click="changeCallback(lang)"
      >
        <q-item-section thumbnail>
          <q-icon v-if="currentLang === lang" name="keyboard_arrow_right" />
        </q-item-section>
        <q-item-section>
          <q-item-label class="lang-label">{{ lang }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
  export default {
    props: ['currentLang', 'changeCallback', 'showHeader'],
  };
</script>

<style lang="sass">
  .lang-label
    text-align: center
    text-transform: uppercase
    font-weight: bold
</style>
