<template>
  <div>
    <v-btn v-for="button in buttons" :key="button"> {{ button }} </v-btn>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  export default {
    computed: {
      ...mapState({
        buttons: (state) => state.meta.navigationButtons,
      }),
    },
  };
</script>
