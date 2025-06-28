import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import Login from '../components/Login.vue'
import Parent_signup from '../components/Parent_signup.vue'
import Side_Panel from '../components/Side_Panel.vue'
import Result from '../components/search_result.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Parent_signup',
      component: Parent_signup,
    },
    {
      path: '/dashboard',
      name: 'Side_Panel',
      component: Side_Panel,
    },
    { path: '/result/:topic', 
      name: 'Result', 
      component: Result, 
      props: true }
  ],
})

export default router
