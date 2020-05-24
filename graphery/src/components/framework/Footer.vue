<template>
  <q-footer>
    <v-card-text
      v-html="footerHtml"
      class="text-center"
      id="footer"
    ></v-card-text>
  </q-footer>
</template>

<script>
  import { mapState } from 'vuex';
  export default {
    computed: {
      ...mapState({
        footerHtml: (state) => state.meta.footerHTML,
      }),
    },
  };
</script>

<style scoped>
  #footer a {
    text-decoration: none;
    color: #bdbdbd !important;
  }
  #footer a:hover {
    color: #fff !important;
  }
  .ft {
    color: #bdbdbd !important;
  }
</style>
