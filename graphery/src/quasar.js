import Vue from 'vue';

import './styles/quasar.sass';
import '@quasar/extras/mdi-v5/mdi-v5.css';
// TODO use material icons instead of mdi icons
import '@quasar/extras/material-icons/material-icons.css';
import { Quasar } from 'quasar';
import Notify from 'quasar/src/plugins/Notify';

Vue.use(Quasar, {
  config: {
    dark: false,
    animations: ['zoomIn', 'zoomOut'],
  },
  components: {
    /* not needed if importStrategy is not 'manual' */
  },
  directives: {
    /* not needed if importStrategy is not 'manual' */
  },
  plugins: {
    Notify,
  },
});
