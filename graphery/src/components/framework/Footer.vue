<template>
  <q-footer elevated reveal class="q-pa-md">
    <!--    TODO change the color in the dark mode    -->
    <div class="text-center" id="footer">
      <div>2020 © Graphery</div>
      <div>
        Built With
        <i class="mdi mdi-heart" style="color: rgb(212, 63, 87);"></i> and
        <a href="https://quasar.dev" target="_blank">Quasar</a>
        powered by
        <a href="https://vuejs.org" target="_blank">Vue</a>
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
    color: #bdbdbd !important;
  }
  .ft {
    color: #bdbdbd !important;
  }
</style>
