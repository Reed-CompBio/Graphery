<script>
  export default {
    data() {
      return {
        currentTab: 'editor',
      };
    },
    methods: {
      onSwitchTabView(tab) {
        this.currentTab = tab;
      },
    },
  };
</script>
