<template>
  <v-footer absolute>
    <v-card-text v-html="footerHtml" class="text-center"></v-card-text>
  </v-footer>
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
