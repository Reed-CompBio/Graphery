<script>
  import { errorDialog } from '../../services/helpers';

  export default {
    data() {
      return {
        showProductGuide_: false,
      };
    },
    computed: {
      showProductGuide() {
        return this.showProductGuide_;
      },
      availableSteps() {
        return [];
      },
    },
    mounted() {
      if (this.showProductGuide) {
        import('intro.js')
          .then((module) => {
            console.debug('intro', module.default);
            const introInstance = module.default();
            introInstance.addSteps(this.availableSteps);
            introInstance.start();
          })
          .catch((err) => {
            errorDialog({ message: `Cannot load intro module. Error: ${err}` });
          });
      }
    },
  };
</script>

<style lang="sass" scoped>
  @import "~intro.js/minified/introjs.min.css"
</style>
