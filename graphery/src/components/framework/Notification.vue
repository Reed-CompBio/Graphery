<template>
  <v-dialog
    persistent
    retain-focus
    scrollable
    max-width="500"
    v-model="show"
    style="z-index: 10000;"
  >
    <v-card>
      <div class="mx-5 mt-5">
        <!-- TODO Invalid prop: custom validator check failed for prop "type". -->
        <v-alert dense outlined :type="'' + status">
          {{ message }}
        </v-alert>
      </div>
      <v-card-text>
        {{ details }}
      </v-card-text>
      <v-card-text v-if="status === 'warning' || status === 'error'">
        I you think there is a problem, please file a issue on
        <a
          href="https://github.com/FlickerSoul/Graphery/issues"
          target="_blank"
          alt="github"
        >
          GitHub </a
        >. Thank you!
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions class="justify-center">
        <v-btn text rounded @click="close">
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';
  export default {
    computed: {
      ...mapState('notifications', ['status', 'message', 'details']),
      ...mapGetters('notifications', ['show']),
    },
    methods: {
      close() {
        console.log('click');
        this.$store.dispatch('notifications/clearNotification');
      },
    },
  };
</script>
