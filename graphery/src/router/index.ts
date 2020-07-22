import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import store from '../store/index';
import { pullUser } from '@/services/helpers';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
  },
  {
    path: '/tutorials',
    name: 'Tutorials',
    component: () =>
      import(/* webpackChunkName: "tutorials" */ '@/views/Tutorials.vue'),
  },
  {
    path: '/tutorial/:url',
    name: 'Tutorial',
    props: true,
    component: () =>
      import(/* webpackChunkName: "tutorial" */ '@/views/Tutorial.vue'),
    children: [
      {
        path: '',
        components: {
          default: () =>
            import(
              /* webpackChunkName: "editor" */
              '@/components/tutorial/Editor.vue'
            ),
          editor: () =>
            import(
              /* webpackChunkName: "editor" */
              '@/components/tutorial/Editor.vue'
            ),
          block: () => import('@/components/framework/LicenseCard.vue'),
        },
      },
    ],
  },
  {
    path: '/graphs',
    name: 'Graphs',
    component: () =>
      import(/* webpackChunkName: "graphs" */ '@/views/Graphs.vue'),
  },
  {
    path: '/graph/:name',
    name: 'Graph',
    props: true,
    component: () =>
      import(/* webpackChunkName: "graph" */ '@/views/Graph.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () =>
      import(/* webpackChunkName: "about" */ '@/views/About.vue'),
  },
  {
    path: '/account',
    name: 'Account',
    component: () =>
      import(/* webpackChunkName: "account" */ '@/views/Account.vue'),
    async beforeEnter(to, from, next) {
      if (store.getters.noUser) {
        await pullUser().catch((_) => null);
        if (store.getters.noUser) {
          next('/login');
          return;
        }
      }
      next();
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: () =>
      import(/* webpackChunkName: "Login" */ '@/views/Login.vue'),
    async beforeEnter(to, from, next) {
      if (store.getters.noUser) {
        await pullUser().catch((_) => null);
        if (store.getters.noUser) {
          next();
          return;
        }
      }
      next('/account');
    },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
  },
  {
    path: '/control-panel',
    component: () => import('@/views/ControlPanel.vue'),
    children: [
      {
        path: '',
        name: 'Control Panel',
        component: () => import('@/components/ControlPanel/MainPage.vue'),
      },
      {
        path: '/tutorial-anchors',
        name: 'Tutorial Anchor List',
        component: () =>
          import('@/components/ControlPanel/TutorialAnchorList.vue'),
      },
    ],
    async beforeEnter(to, from, next) {
      if (store.state['user'] === null) {
        await pullUser().catch((_) => null);
        if (store.state['user'] === null) {
          next('/login');
          return;
        }
      }

      if (store.state['user'].role === 'Visitor') {
        next('/account');
      } else {
        next();
      }
    },
  },
  {
    path: '/*',
    name: '404',
    component: () =>
      import(/* webpackChunkName: "settings" */ '@/views/404.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
