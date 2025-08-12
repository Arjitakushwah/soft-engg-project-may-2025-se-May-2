import { createRouter, createWebHistory } from 'vue-router'

// Import your components
import HomePage from '../components/HomePage.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AddChild from '../components/AddChild.vue'
import ParentDashboard from '../components/ParentDashboard.vue'
import ChildDashboard from '../components/ChildDashboard.vue'
import ChildCalender from '../components/ChildCalender.vue'
import ChildStory from '../components/ChildStory.vue'
import ChildToDoList from '../components/ChildToDoList.vue'
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
import Error404 from '../components/Error404.vue'
import ParentEditProfile from '../components/ParentEditProfile.vue'
import ChildEditProfile from '../components/ChildEditProfile.vue'
import GoogleAuthCallback from '../components/GoogleAuthCallBack.vue'

const routes = [
  // --- PUBLIC ROUTES ---
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },
  { path: '/forgot-username', name: 'ForgotUsername', component: ForgotUsername },
  { path: '/checkotp', name: 'VerifyOTP', component: VerifyOTP },
  { path: '/resetpassword', name: 'ResetPassword', component: ResetPassword },
  { path: '/error-404', name: 'Error404', component: Error404 },
  {
    path: '/auth/google/callback',
    name: 'GoogleAuthCallback',
    component: GoogleAuthCallback
  },

  // --- CHILD PROTECTED ROUTES ---
  {
    path: '/child',
    component: ChildDashboard,
    name: 'Child',
    meta: { requiresAuth: true, role: 'child' }, // Meta field for protection
    children: [
      { path: 'home', name: 'ChildHome', component: ChildHome },
      { path: 'calendar', name: 'ChildCalender', component: ChildCalender },
      { path: 'todo', name: 'ChildToDoList', component: ChildToDoList },
      { path: 'story', name: 'ChildStory', component: ChildStory },
      { path: 'journal', name: 'ChildJournal', component: ChildJournal },
      { path: 'infotainment', name: 'ChildInfotainment', component: ChildInfotainment },
      { path: 'result', name: 'infoResult', component: Result, props: true },
      { path: 'edit-profile', name: 'ChildEditProfile', component: ChildEditProfile }
    ]
  },

  // --- PARENT PROTECTED ROUTES ---
  {
    path: '/parent',
    component: ParentDashboard,
    name: 'Parent',
    meta: { requiresAuth: true, role: 'parent' }, // Meta field for protection
    children: [
      { path: 'home', name: 'ParentHome', component: ParentHome },
      { path: 'add-child', name: 'AddChild', component: AddChild },
      { path: 'calendar', name: 'ParentCalendar', component: ParentCalendar },
      {
        path: 'activity_analysis',
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
  },

  // Catch-all route for 404 errors
  { path: '/:pathMatch(.*)*', redirect: '/error-404' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- GLOBAL NAVIGATION GUARD ---
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiredRole = to.meta.role;
  const token = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('userRole');

  if (requiresAuth) {
    // 1. If route requires auth and user is not logged in, redirect to login
    if (!token) {
      next({ name: 'Login' });
    } else {
      // 2. If user is logged in but does not have the required role, redirect them
      if (requiredRole && userRole !== requiredRole) {
        // Redirect to their own dashboard based on their actual role
        if (userRole === 'parent') {
          next({ name: 'ParentHome' });
        } else if (userRole === 'child') {
          next({ name: 'ChildHome' });
        } else {
          // Fallback to login if role is unknown
          next({ name: 'Login' });
        }
      } else {
        // 3. If user is authenticated and has the correct role, proceed
        next();
      }
    }
  } else {
    // 4. For public routes, just proceed
    next();
  }
});

export default router;
