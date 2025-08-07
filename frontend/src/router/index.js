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
// import QuizPage from '../components/QuizPage.vue'
import ParentCalendar from '../components/ParentCalendar.vue'
import ParentJournalAnalysis from '../components/ParentJournalAnalysis.vue'
import ChildHome from '../components/ChildHome.vue'
import ParentHome from '../components/ParentHome.vue'
import ChildJournal from '../components/ChildJournal.vue'
import ChildInfotainment from '../components/ChildInfotainment.vue'
import Result from '../components/InfoResult.vue'
import ParentActivityInsight from '../components/ParentActivityInsight.vue'
import ParentToDoInsight from '../components/ParentToDoInsight.vue'
import ParentStoryInsight from '../components/ParentStoryInsight.vue'
import ParentInfotainmentInsight from '../components/ParentInfotainmentInsight.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import ForgotUsername from '../components/ForgotUsername.vue'
import VerifyOTP from '../components/checkotp.vue'
import ResetPassword from '../components/ResetPassword.vue'
import ParentEditProfile from '../components/ParentEditProfile.vue'
import ChildEditProfile from '../components/ChildEditProfile.vue'

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },
  { path: '/forgot-username', name: 'ForgotUsername', component: ForgotUsername },
  { path: '/checkotp', name: 'VerifyOTP', component: VerifyOTP },
  { path: '/resetpassword', name: 'ResetPassword', component: ResetPassword },

  {
    path: '/child',
    component: ChildDashboard,
    name: 'Child',
    children: [
      { path: 'home', name: 'ChildHome', component: ChildHome },
      { path: 'calendar', name: 'ChildCalender', component: ChildCalender },
      { path: 'todo', name: 'ChildToDoList', component: ChildToDoList },
      { path: 'story', name: 'ChildStory', component: ChildStory },
      // { path: 'quiz', name: 'QuizPage', component: QuizPage },
      { path: 'journal', name: 'ChildJournal', component: ChildJournal },
      { path: 'infotainment', name: 'ChildInfotainment', component: ChildInfotainment },
      { path: 'result', name: 'InfoResult', component: Result, props: true },
      { path: 'edit-profile', name: 'ChildEditProfile', component: ChildEditProfile }
    ]
  },

  {
    path: '/parent',
    component: ParentDashboard,
    name: 'Parent',
    children: [
      { path: 'home', name: 'ParentHome', component: ParentHome },
      { path: 'add-child', name: 'AddChild', component: AddChild },
      { path: 'calendar', name: 'ParentCalendar', component: ParentCalendar },
      {
        path: 'activity-analysis',
        component: ParentActivityInsight,
        name: 'ParentActivityInsight',
        children: [
          { path: 'journal', name: 'ParentJournalAnalysis', component: ParentJournalAnalysis },
          { path: 'to-do-list', name: 'ParentToDoInsight', component: ParentToDoInsight },
          { path: 'story', name: 'ParentStoryInsight', component: ParentStoryInsight },
          { path: 'infotainment', name: 'ParentInfotainmentInsight', component: ParentInfotainmentInsight }
        ]
      },
      { path: 'edit-profile', name: 'ParentEditProfile', component: ParentEditProfile }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
