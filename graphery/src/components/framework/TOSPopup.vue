<script>
  import { Notify } from 'quasar';

  export default {
    methods: {
      jumpToTOS() {
        this.$router.push({ name: 'TOS' });
      },
      agreeTos() {
        this.$store.commit('settings/CHANGE_TOS_AGREE_AND_NOT_SHOW', true);
      },
      showTOSTerms() {
        if (!this.$store.state.settings.tosAgreeAndDoNotShowAgain) {
          Notify.create({
            type: 'gdpr',
            caption:
              'By continuing to access Graphery, you agree to the terms of service and privacy notice',
            message: 'Cookies helps us improve your experience',
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
                label: 'Close',
                color: 'white',
                handler: this.agreeTos,
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
