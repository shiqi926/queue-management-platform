import { createRouter, createWebHistory } from 'vue-router'
import Welcome from '../views/Welcome.vue'
import Gallery from '../views/Gallery.vue'
import Panel from '../views/Panel.vue'
import Dashboard from '../views/Dashboard.vue'
//import {firebaseAuth} from '@/main.js';
import firebase from "firebase/app"

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: Gallery,
    meta: {
      authRequired: true,
    }
  },
  {
    path: '/panel',
    name: 'Panel',
    component: Panel,
    meta: {
      authRequired: true,
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      authRequired: true,
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.authRequired)) {
    if (firebase.auth().currentUser) {
      next();
    } else {
      alert('You must be logged in to see this page');
      next({
        path: '/',
      });
    }
  } else {
    next();
  }
});

// router.beforeEach((to, from, next) => {
//   const currentUser = firebase.auth().currentUser;
//   const requiresAuth = to.matched.some(record=> record.meta.requiresAuth);
//   if (requiresAuth && currentUser) next ('home');
//   else next();
// });

export default router
