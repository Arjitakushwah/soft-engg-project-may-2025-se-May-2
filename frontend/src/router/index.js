import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AddChild from '../components/AddChild.vue'
import ParentDashboard from '../components/ParentDashboard.vue'
import ChildDashboard from '../components/ChildDashboard.vue'
import ChildCalendar from '../components/ChildCalendar.vue'
import ChildToDoList from '../components/ChildToDoList.vue'
import ChildStory from '../components/ChildStory.vue'
import QuizPage from '../components/QuizPage.vue'


const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/add-child', name: 'AddChild', component: AddChild },
  { path: '/parent_dashboard', name: 'ParentDashboard', component: ParentDashboard },
  { path: '/child_dashboard', name: 'ChildDashboard', component: ChildDashboard },
  { path: '/child_calendar', name: 'ChildCalendar', component: ChildCalendar },
  { path: '/child_todolist', name: 'ChildToDoList', component: ChildToDoList },
  { path: '/child_story', name: 'ChildStory', component: ChildStory },
  { path: '/quiz', name: 'QuizPage', component: QuizPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router