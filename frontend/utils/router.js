import Home from '../pages/Home.js';

const routes = [
  {
    path: '/',
    component: Home
  }
  // Add more routes as needed
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;
