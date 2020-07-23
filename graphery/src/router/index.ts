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
    props: true,
    component: () =>
      import(/* webpackChunkName: "tutorial" */ '@/views/Tutorial.vue'),
    children: [
      {
        path: '',
        name: 'Tutorial',
        components: {
          default: () =>
            import(
              /* webpackChunkName: "editor" */
              '@/components/tutorial/Editor.vue'
            ),
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
        redirect: { name: 'Control Panel' },
      },
      {
        path: 'main',
        name: 'Control Panel',
        component: () => import('@/components/ControlPanel/MainPage.vue'),
      },
      {
        path: 'categories',
        name: 'Category List',
        component: () =>
          import('@/components/ControlPanel/lists/CategoryList.vue'),
      },
      {
        path: 'tutorial-anchors',
        name: 'Tutorial Anchor List',
        component: () =>
          import('@/components/ControlPanel/lists/TutorialAnchorList.vue'),
      },
      {
        path: 'tutorial-anchor-editor/:url',
        name: 'Tutorial Anchor Editor',
        props: true,
        component: () =>
          import(
            '@/components/ControlPanel/editors/TutorialAnchorCreation.vue'
          ),
      },
      {
        path: 'tutorial-content',
        name: 'Tutorial Content List',
        component: () =>
          import('@/components/ControlPanel/lists/TutorialContentList.vue'),
      },
      {
        path: 'tutorial-content-editor/:url',
        name: 'Tutorial Content Editor',
        props: true,
        component: () =>
          import(
            '@/components/ControlPanel/editors/TutorialContentCreation.vue'
          ),
      },
      {
        path: 'graphs',
        name: 'Graph List',
        component: () =>
          import('@/components/ControlPanel/lists/GraphList.vue'),
      },
      {
        path: 'graph-editor/:url',
        name: 'Graph Editor',
        props: true,
        component: () =>
          import('@/components/ControlPanel/editors/GraphCreation.vue'),
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
