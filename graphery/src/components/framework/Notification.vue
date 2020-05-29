<template>
  <q-dialog
    persistent
    transition-show="slide-down"
    transition-hide="slide-down"
    scrollable
    v-model="show"
    class="notification"
  >
    <q-card>
      <div class="q-ma-sm">
        <q-item>
          <q-item-section avatar>
            <q-icon :name="icon" :color="color" size="md"></q-icon>
          </q-item-section>
          <q-item-section>
            <div class="popup-message">
              {{ message }}
            </div>
          </q-item-section>
        </q-item>
      </div>
      <q-card>
        <q-card-section>
          {{ details }}
        </q-card-section>
      </q-card>
      <q-card-actions align="right">
        <q-btn flat icon="mdi-menu-down" @click="toggleMore"></q-btn>
        <q-btn flat label="OK" @click="close"> </q-btn>
      </q-card-actions>
      <q-slide-transition style="max-width: 100%;">
        <div v-show="more" style="width: inherit">
          <q-card>
            <q-card-section>
              I you think there is a problem, <br />please file a issue on
              <a
                href="https://github.com/FlickerSoul/Graphery/issues"
                target="_blank"
              >
                GitHub </a
              >. Thank you!
            </q-card-section>
          </q-card>
        </div>
      </q-slide-transition>
    </q-card>
  </q-dialog>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';
  import { NotificationStatus } from '../../store/states/state';

  export default {
    data() {
      return {
        more: false,
      };
    },
    computed: {
      ...mapState('notifications', ['status', 'message', 'details']),
      ...mapGetters('notifications', ['show']),
      icon() {
        switch (this.status) {
          case NotificationStatus.success:
            return 'mdi-checkbox-marked-circle';
          case NotificationStatus.info:
            return 'mdi-information';
          case NotificationStatus.warning:
            return 'mdi-emoticon-neutral';
          case NotificationStatus.error:
            return 'mdi-cancel';
          default:
            return '';
        }
      },
      color() {
        switch (this.status) {
          case NotificationStatus.success:
            return 'positive';
          case NotificationStatus.info:
            return 'info';
          case NotificationStatus.warning:
            return 'warning';
          case NotificationStatus.error:
            return 'negative';
          default:
            return '';
        }
      },
    },
    methods: {
      close() {
        this.$store.dispatch('notifications/clearNotification');
      },
      toggleMore() {
        this.more = !this.more;
      },
    },
  };
</script>

<style scoped>
  .notification {
    z-index: 10000;
    max-width: 500px;
    min-width: 230px;
  }
</style>
