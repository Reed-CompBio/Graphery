import Vue from 'vue';

import './styles/quasar.sass';
import { Quasar } from 'quasar';

Vue.use(Quasar, {
  config: {
    iconSet: 'mdi-v4',
    dark: true,
  },
  components: {
    /* not needed if importStrategy is not 'manual' */
  },
  directives: {
    /* not needed if importStrategy is not 'manual' */
  },
  plugins: {},
});
