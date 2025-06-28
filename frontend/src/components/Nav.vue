<!-- src/components/Nav.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- App Name -->
      <router-link to="/" class="navbar-brand app-title">Skill Explorers</router-link>

      <!-- Greeting -->
      <span v-if="userRole !== 'guest'" class="me-3 welcome-text">
        Welcome, {{ username }}!
      </span>

      <!-- Navigation Buttons -->
      <div class="d-flex">
        <!-- Guest -->
        <template v-if="userRole === 'guest'">
          <router-link to="/login" class="btn btn-outline-primary me-2">Login</router-link>
          <router-link to="/register" class="btn btn-primary">Register</router-link>
        </template>

        <!-- Parent -->
        <template v-else-if="userRole === 'parent'">
          <button @click="goToDashboard" class="btn btn-outline-success me-2">Dashboard</button>
          <button @click="logout" class="btn btn-danger">Logout</button>
        </template>

        <!-- Child -->
        <template v-else-if="userRole === 'child'">
          <button @click="goToDashboard" class="btn btn-outline-success me-2">My Dashboard</button>
          <button @click="logout" class="btn btn-danger">Logout</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const emit = defineEmits(['navigate', 'logout'])

const userRole = ref('guest')
const username = ref('')

onMounted(() => {
  userRole.value = localStorage.getItem('userRole') || 'guest'
  username.value = localStorage.getItem('username') || ''
})

const goToDashboard = () => {
  const role = localStorage.getItem('userRole')
  if (role === 'child') {
    router.push({ path: '/child_dashboard' })
  } else if (role === 'parent') {
    router.push({ path:'/Parent_Dashboard' })
  }
}

const logout = () => {
  localStorage.clear()
  router.push({ path: '/' })
}
</script>

<style scoped>
.navbar {
  background-color: #f4cfc5 !important; /* Light blue */
  border-bottom: 1px solid #cbd5e1;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: #1e3a8a !important; /* Dark blue */
  text-decoration: none;
}

.welcome-text {
  font-family: 'Comic Neue', cursive;
  font-size: 2rem;
  font-weight: bold;
  color: #1e3a8a;
}

/* Buttons */
.btn-outline-primary {
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-outline-primary:hover {
  background-color: #3b82f6;
  color: white;
}

.btn-primary {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

.btn-primary:hover {
  background-color: #2563eb;
  border-color: #2563eb;
}

.btn-outline-success {
  border-color: #1e3a8a;
  color: #1e3a8a;
}

.btn-outline-success:hover {
  background-color: #1e3a8a;
  color: white;
}

.btn-danger {
  background-color: #ef4444;
  border-color: #ef4444;
}

.btn-danger:hover {
  background-color: #dc2626;
  border-color: #dc2626;
}
</style>
