<script>
  import { errorDialog } from '../../services/helpers';

  export default {
    data() {
      return {
        introInstance: null,
        shouldLoad_: true,
      };
    },
    computed: {
      shouldLoad() {
        return this.shouldLoad_;
      },
    },
    methods: {
      addIntroSteps(steps) {
        this.introInstance?.addSteps(steps);
      },
      setIntroSteps(steps) {
        this.introInstance?.setOption('steps', steps);
      },
      setIntroOptions(optionKey, optionValue) {
        this.introInstance?.setOption(optionKey, optionValue);
      },
      startIntro() {
        this.introInstance?.start();
      },
      onCompleteCallback() {
        return undefined;
      },
      onBeforeExitCallback() {
        return true;
      },
      onExitCallback() {
        return undefined;
      },
      async loadIntroModule() {
        if (!this.shouldLoad) {
          return this.introInstance;
        }

        if (this.introInstance === null) {
          await import('intro.js')
            .then((module) => {
              console.debug('intro', module.default);
              this.introInstance = module
                .default()
                .setOption('tooltipClass', 'customTooltip')
                .oncomplete(this.onCompleteCallback)
                .onbeforeexit(this.onBeforeExitCallback)
                .onexit(this.onExitCallback);
            })
            .catch((err) => {
              errorDialog({
                message: `Cannot load intro module. Error: ${err}`,
              });
            });
        }

        return this.introInstance;
      },
    },
  };
</script>

<style lang="sass">
  @import "~intro.js/minified/introjs.min.css"
  @import "~intro.js/themes/introjs-modern.css"

  .customTooltip
    max-width: 500px
    .introjs-tooltip-title
      font-size: 1.2rem
    .introjs-tooltiptext
      font-size: 1rem

  .introjs-helperLayer
    box-shadow: rgb(33 33 33 / 80%) 0px 0px 1px 2px, rgb(33 33 33 / 70%) 0px 0px 0px 5000px !important
</style>
