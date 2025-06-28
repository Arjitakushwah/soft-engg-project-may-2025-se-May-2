<template>
  <header class="dashboard-header">
    <div class="branding">
      <button class="home-button" @click="goHome">🏠</button>
      <h2 class="greeting">
        Hi, <span class="username">{{ displayName }}</span>
      </h2>
    </div>

    <div class="nav-actions">
      <button v-if="role === 'child'" @click="goToChildDashboard" class="logout-button">Dashboard</button>
      <button v-if="role === 'parent'" @click="goToParentDashboard" class="logout-button">Dashboard</button>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const role = ref('')
const displayName = ref('User')

onMounted(() => {
  role.value = localStorage.getItem('role') || ''
  const name = localStorage.getItem('name') || 'User'
  displayName.value = name
})

const goToChildDashboard = () => {
  if (router.currentRoute.value.path !== '/child_dashboard') {
    router.push('/child_dashboard')
  }
}

const goToParentDashboard = () => {
  if (router.currentRoute.value.path !== '/parent_dashboard') {
    router.push('/parent_dashboard')
  }
}

const goHome = () => {
  router.push('/')
}

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: #1e1e2f;
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.branding {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.greeting {
  font-size: 1.6rem;
  margin: 0;
}

.username {
  color: #00f7ff;
}

.nav-actions {
  display: flex;
  gap: 1rem;
}

.logout-button,
.home-button {
  background-color: #ff4757;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover,
.home-button:hover {
  background-color: #e63946;
}
</style>
