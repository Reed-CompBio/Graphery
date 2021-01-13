<template>
  <div id="footer-wrapper" class="q-pa-md full-width">
    <!--    TODO change the color in the dark mode    -->
    <div class="text-center grey-a" id="footer">
      <div>
        2020 ©
        <router-link :to="{ name: 'About' }">
          Graphery
        </router-link>
        |
        <a
          href="https://github.com/FlickerSoul/Graphery"
          target="_blank"
          rel="noreferrer"
        >
          <i class="mdi mdi-github icon-adjust"></i>GitHub |
        </a>
        <span class="feedback">
          <i class="mdi mdi-comment-question icon-adjust"></i>Feedback
          <!-- TODO: hovering content change (github issues, email) -->
        </span>
      </div>
      <div>
        Built with
        <i class="mdi mdi-heart" style="color: rgb(212, 63, 87);"></i> and
        <a href="https://quasar.dev" target="_blank" rel="noreferrer">Quasar</a>
        <!-- TODO: import Quasar SVG as font icon / ref to iconmoon -->
        Powered by
        <a href="https://vuejs.org" target="_blank" rel="noreferrer">
          <i class="mdi mdi-vuejs icon-adjust"></i>Vue
        </a>
      </div>
    </div>
  </div>
</template>

<style lang="sass">
  .grey-a a
    color: grey
    text-decoration: none
    &:hover
      color: #464646
  #footer-wrapper
    /* TODO change the font color */
    color: grey
    margin-top: 32px
    margin-bottom: 48px
  .icon-adjust
    margin-right: 1px
</style>
