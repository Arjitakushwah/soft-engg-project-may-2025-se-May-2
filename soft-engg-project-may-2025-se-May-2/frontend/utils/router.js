import Home from '../pages/Home.js';
import Login from '../pages/Login.js';
import Signup from '../pages/Parent_signup.js';
import ChildDash from '../pages/Child_dash.js';
import CalendarReport from '../pages/Child_CalendarReport.js';
import ToDoList from '../pages/Child_ToDoList.js';
import StoryPage from '../pages/Child_Story.js';

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/register',
    component: Signup
  },
  {
    path: '/child_dash',
    component: ChildDash
  },
  { 
    path: '/calendar', 
    component: CalendarReport 
  },
  { 
    path: '/todolist', 
    component: ToDoList 
  },
  { 
    path: '/storypage', 
    component: StoryPage 
  },

  // Add more routes as needed
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;
