<script>
  export default {
    data() {
      return {
        tableLang: this.$i18n.locale,
      };
    },
    methods: {
      changeTableLang(lang) {
        this.tableLang = lang;
      },
    },
  };
</script>
