<template>
  <v-dialog persistent retain-focus scrollable max-width="500" v-model="show">
    <v-card>
      <v-card-title primary-title class="headline lighten-2">
        <v-icon :color="whichColor">{{ iconType }} </v-icon>
        <div class="pa-1">{{ message }}</div>
      </v-card-title>
      <v-card-text>
        {{ details }}
      </v-card-text>
      <v-card-text v-if="warning || error">
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
      ...mapState('notifications', [
        'info',
        'warning',
        'error',
        'message',
        'details',
      ]),
      ...mapGetters('notifications', ['show']),
      iconType() {
        if (this.info) {
          return 'mdi-information';
        } else if (this.warning) {
          return 'mdi-comment-processing';
        } else if (this.error) {
          return 'mdi-close-circle';
        } else {
          return '';
        }
      },
      whichColor() {
        if (this.info) {
          return 'info';
        } else if (this.warning) {
          return 'warning';
        } else if (this.error) {
          return 'error';
        } else {
          return '';
        }
      },
    },
    methods: {
      close() {
        console.log('click');
        this.$store.dispatch('notifications/clearNotification');
      },
    },
  };
</script>
