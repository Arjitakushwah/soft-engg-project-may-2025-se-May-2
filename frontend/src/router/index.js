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
import JournalAnalysis from '../components/ParentJournalAnalysis.vue'
import ChildHome from '../components/ChildHome.vue'
import ParentHome from '../components/ParentHome.vue'
import ChildJournal from '../components/ChildJournal.vue'
import ChildInfotainment from '../components/ChildInfotainment.vue'
import Result from '../components/InfoResult.vue'
import ParentActivityInsight from '../components/ParentActivityInsight.vue'
import ParentJournalAnalysis from '../components/ParentJournalAnalysis.vue'
import ParentToDoInsight from '../components/ParentToDoInsight.vue'
import ParentStoryInsight from '../components/ParentStoryInsight.vue'
import ParentInfotainmentInsight from '../components/ParentInfotainmentInsight.vue'

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },

  {
    path: '/child', name: 'Child', component: ChildDashboard,
    children: [
      { path: 'home', name: 'ChildDashboard', component: ChildHome },
      { path: 'calendar', name: 'ChildCalender', component: ChildCalender },
      { path: 'todo', name: 'ChildToDoList', component: ChildToDoList },
      { path: 'story', name: 'ChildStory', component: ChildStory },
      // { path: 'quiz', name: 'QuizPage', component: QuizPage },
      { path: 'journal', name: 'ChildJournal', component: ChildJournal },
      { path: 'infotainment', name: 'ChildInfotainment', component: ChildInfotainment },
      { path: 'result/:topic', name: 'Result', component: Result, props: true }
    ]
  },
  {
    path: '/parent', component: ParentDashboard, name: 'Parent',
    children: [
      {path: 'home', name: 'ParentDashboard', component: ParentHome},
      {path: 'add_child',name: 'AddChild', component: AddChild},
      {path: 'calendar', name: 'ParentCalendar', component: ParentCalendar},
      {path: 'activity_analysis', name: 'ParentActivityInsight', component: ParentActivityInsight,
      children: [
        { path: 'journal', component: ParentJournalAnalysis },
        { path: 'to-do-list', component: ParentToDoInsight },
        { path: 'story', component: ParentStoryInsight },
        { path: 'infotainment', component: ParentInfotainmentInsight},
      ]},

    ],
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
