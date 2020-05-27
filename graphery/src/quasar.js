import Vue from 'vue';

import './styles/quasar.sass';
import '@quasar/extras/mdi-v5/mdi-v5.css';
import '@quasar/extras/material-icons/material-icons.css';
import { Quasar } from 'quasar';

Vue.use(Quasar, {
  config: {
    iconSet: 'mdi-v5',
    dark: false,
    animations: ['zoomIn', 'zoomOut'],
  },
  components: {
    /* not needed if importStrategy is not 'manual' */
  },
  directives: {
    /* not needed if importStrategy is not 'manual' */
  },
  plugins: {},
});
