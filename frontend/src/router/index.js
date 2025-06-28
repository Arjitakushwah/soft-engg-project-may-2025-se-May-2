import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../components/HomePage.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AddChild from '../components/AddChild.vue'
import ParentDashboard from '../components/ParentDashboard.vue'
import ChildDashboard from '../components/ChildDashboard.vue'
import ChildCalender from '../components/ChildCalender.vue'
import ChildStory from '../components/ChildStory.vue'
import ChildToDoList from '../components/ChildToDoList.vue'
import QuizPage from '../components/QuizPage.vue'
import ParentCalendar from '../components/ParentCalendar.vue'
import ParentJournalAnalysis from '../components/ParentJournalAnalysis.vue'
import ChildHome from '../components/ChildHome.vue'
import ParentHome from '../components/ParentHome.vue'
import ChildJournal from '../components/ChildJournal.vue'
import ChildInfotainment from '../components/ChildInfotainment.vue'
import Result from '../components/InfoResult.vue'

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/add-child', name: 'AddChild', component: AddChild },
  { path: '/parent_dashboard', name: 'ParentDashboard', component: ParentDashboard },
  {
    path: '/child_dashboard',
    name: 'ChildDashboard',
    component: ChildDashboard,
    children: [
      { path: '', name: 'dashboard_child', component: ChildHome }, // default route
      { path: 'calendar', name: 'ChildCalender', component: ChildCalender },
      { path: 'todo', name: 'ChildToDoList', component: ChildToDoList },
      { path: 'story', name: 'ChildStory', component: ChildStory },
      { path: 'quiz', name: 'QuizPage', component: QuizPage },
      { path: 'journal', name: 'ChildJournal', component: ChildJournal },
      { path: 'infotainment', name: 'ChildInfotainment', component: ChildInfotainment },
      { path: 'result/:topic', name: 'Result', component: Result, props: true }
    ]
  },
  {
    path: '/parent_dashboard',
    component: ParentDashboard,
    name:'ParentDashboard',
    children: [
      {
        path: '',
        name: 'dashboard_parent',
        component: ParentHome, // ✅ Use this as default dashboard
      },
      {
        path: 'add_child',
        name: 'AddChild',
        component: AddChild,
      },
      {
        path: 'calendar',
        name: 'ParentCalendar',
        component: ParentCalendar,
      },
      {
        path: 'journal_analysis',
        name: 'ParentJournalAnalysis',
        component: ParentJournalAnalysis,
      },
    ],
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
