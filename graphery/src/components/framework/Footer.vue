<template>
  <div id="footer-wrapper" class="q-pa-md full-width">
    <!--    TODO change the color in the dark mode    -->
    <div class="text-center grey-a" id="footer">
      <div>
        2020 © Graphery |
        <a
          href="https://github.com/FlickerSoul/Graphery"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>
      </div>
      <div>
        Built With
        <i class="mdi mdi-heart" style="color: rgb(212, 63, 87);"></i> and
        <a href="https://quasar.dev" target="_blank" rel="noreferrer">Quasar</a>
        powered by
        <a href="https://vuejs.org" target="_blank" rel="noreferrer">Vue</a>
      </div>
    </div>
  </div>
</template>

<style lang="sass">
  .grey-a a
    color: grey
    text-decoration: underline
  #footer-wrapper
    /* TODO change the font color */
    color: grey
    margin-top: 32px
    margin-bottom: 48px
</style>
