<template>
  <q-footer elevated reveal class="q-pa-md">
    <!--    TODO change the color in the dark mode    -->
    <div class="text-center" id="footer">
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
  </q-footer>
</template>

<style scoped>
  #footer a,
  #footer a:visited {
    color: #fff !important;
  }
  #footer a:hover {
    color: #cfcfcf !important;
  }
</style>
