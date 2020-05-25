import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/tutorials',
    name: 'Tutorials',
    component: () => import('@/views/Tutorials.vue'),
  },
  {
    path: '/tutorial/:name',
    name: 'Tutorial',
    props: true,
    component: () => import('@/views/Tutorial.vue'),
  },
  {
    path: '/graphs',
    name: 'Graphs',
    component: () => import('@/views/Graphs.vue'),
  },
  {
    path: '/graph/:name',
    name: 'Graph',
    props: true,
    component: () => import('@/views/Graph.vue'),
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
    component: () => import('@/views/Account.vue'),
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
  },
  { path: '/*', name: '404', component: () => import('@/views/404.vue') },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
