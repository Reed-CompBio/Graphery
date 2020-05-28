import Vue from 'vue';

import './styles/quasar.sass';
import '@quasar/extras/mdi-v5/mdi-v5.css';
// TODO use material icons instead of mdi icons
import '@quasar/extras/material-icons/material-icons.css';
import { Quasar } from 'quasar';
import Notify from 'quasar/src/plugins/Notify';
import LocalStorage from 'quasar/src/plugins/LocalStorage';

Vue.use(Quasar, {
  config: {
    iconSet: 'mdi-v5',
    dark: false,
    animations: ['zoomIn', 'zoomOut'],
    importStrategy: 'manual',
    // not working???
  },
  components: {
    /* not needed if importStrategy is not 'manual' */
  },
  directives: {
    /* not needed if importStrategy is not 'manual' */
  },
  plugins: {
    Notify,
    LocalStorage,
  },
});
