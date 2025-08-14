<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- App Title -->
      <div class="d-flex align-items-center gap-3">
        <!-- Hamburger for mobile -->
        <button
          class="btn d-md-none"
          @click="$emit('toggle-sidebar')"
          aria-label="Toggle sidebar"
        >
          <i class="bi bi-list fs-3"></i>
        </button>

        <router-link to="/" class="navbar-brand app-title">
          Skill Explorers
        </router-link>
      </div>

      <!-- Welcome Text -->
      <span class="me-3 welcome-text d-none d-md-inline">
        Welcome, {{ username }}!
      </span>

      <!-- Action Buttons -->
      <div class="d-flex">
        <template v-if="userRole === 'parent'">
          <button @click="goToDashboard" class="btn btn-outline-success me-2">Dashboard</button>
          <button class="btn btn-primary me-2" @click="navigateToPage('ParentEditProfile')">Edit Profile</button>
          <button @click="logout" class="btn btn-danger">Logout</button>
        </template>
        <template v-else-if="userRole === 'child'">
          <button @click="goToDashboard" class="btn btn-outline-success me-2">My Dashboard</button>
          <button class="btn btn-primary me-2" @click="navigateToPage('ChildEditProfile')">Edit Profile</button>
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
const emit = defineEmits(['navigate', 'logout', 'toggle-sidebar'])

const userRole = ref('')
const username = ref('')

onMounted(() => {
  userRole.value = localStorage.getItem('userRole')
  username.value = localStorage.getItem('username') || ''
})

const goToDashboard = () => {
  const role = localStorage.getItem('userRole')
  if (role === 'child') {
    router.push({ path: '/child/home' })
  } else if (role === 'parent') {
    router.push({ path: '/Parent/home' })
  }
}

const logout = () => {
  localStorage.clear()
  router.push({ path: '/' })
}

const navigateToPage = (page) => {
  console.log('Navigating to:', page)
  router.push({ name: page })
}

</script>

<style scoped>
.navbar {
  background-color: #E6E6FA !important;
}

.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: #1e3a8a !important;
  text-decoration: none;
}

.welcome-text {
  font-family: 'Comic Neue', cursive;
  font-size: 2rem;
  font-weight: bold;
  color: #1e3a8a;
}

.btn-outline-primary {
  background-color: white;
  border-color: #3b82f6;
  color: #ff6a88;
  border: none;
  margin-left: 10px;
  padding: 10px 20px;
  font-family: 'Fredoka One', cursive;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.btn-outline-primary:hover {
  transform: scale(1.05);
  background-color: #faf2f4;
}

.btn-outline-success {
  background: white;
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
