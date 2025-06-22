import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AddChild from '../components/AddChild.vue'
import ParentDashboard from '../components/ParentDashboard.vue'
import ChildDashboard from '../components/ChildDashboard.vue'

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/add-child', name: 'AddChild', component: AddChild },
  { path: '/parent_dashboard', name: 'ParentDashboard', component: ParentDashboard },
  { path: '/child_dashboard', name: 'ChildDashboard', component: ChildDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router