import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';

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
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ '@/views/About.vue'),
  },
  {
    path: '/account',
    name: 'Account',
    component: () =>
      import(/* webpackChunkName: "account" */ '@/views/Account.vue'),
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
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
