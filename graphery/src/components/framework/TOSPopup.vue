<script>
  import { Notify } from 'quasar';

  export default {
    data() {
      return {
        tosVersion_: '0.0.1',
      };
    },
    computed: {
      isShowingTOS() {
        return !(
          this.$store.state.settings.tosAgreeAndDoNotShowAgain &&
          this.$store.state.settings.tosVersion === this.tosVersion_
        );
      },
      selectMessage() {
        if (this.$store.state.settings.tosVersion === this.tosVersion_) {
          return 'Cookies helps us improve your experience';
        } else {
          return '[TOS Updated] Cookies helps us improve your experience';
        }
      },
    },
    methods: {
      jumpToTOS() {
        this.$router.push({ name: 'TOS' });
      },
      agreeTos() {
        this.$store.commit('settings/CHANGE_TOS_AGREE_AND_NOT_SHOW', true);
        this.$store.commit('settings/CHANGE_TOS_VERSION', this.tosVersion_);
      },
      showTOSTerms() {
        if (this.isShowingTOS) {
          Notify.create({
            type: 'gdpr',
            caption:
              'By continuing to access Graphery, you agree to the terms of service and privacy notice',
            message: this.selectMessage,
            group: false,
            timeout: 0,
            multiLine: true,
            actions: [
              {
                label: 'Learn more',
                color: 'warning',
                handler: this.jumpToTOS,
              },
              {
                label: 'Never Show Again',
                color: 'white',
                handler: this.agreeTos,
              },
              {
                label: 'Close',
                color: 'white',
              },
            ],
          });
        }
      },
    },
    created() {
      this.$q.notify.registerType('gdpr', {
        icon: 'privacy_tip',
        // color: 'grey',
        textColor: 'white',
        position: 'bottom-right',
        classes: 'gdpr',
      });
    },
  };
</script>

<style lang="sass" scoped>
  .gdpr
    max-width: 350px !important
</style>
