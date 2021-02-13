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
            type: 'warning',
            caption: 'Agreement',
            message:
              'By proceeding you agree to the terms of service and privacy notice',
            group: false,
            timeout: 0,
            multiLine: true,
            actions: [
              {
                label: 'Read the terms of service and privacy notices',
                color: 'primary',
                handler: this.jumpToTOS,
              },
              {
                label: 'Agree and never show again',
                color: 'white',
                handler: this.agreeTos,
              },
            ],
          });
        }
      },
    },
  };
</script>
