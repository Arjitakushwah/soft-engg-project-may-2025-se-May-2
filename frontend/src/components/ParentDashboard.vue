<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h2>Hi {{ parentName }}</h2>
      <h2 class="welcome">Welcome to your Parent Dashboard</h2>
      <button @click="logout" class="logout-button">Logout</button>
    </header>

    <div class="dashboard-body">
      <aside class="sidebar">
        <router-link to="/add-child" class="sidebar-link">➕ Add Child</router-link>
        <router-link to="/child-activity" class="sidebar-link">📊 View Child Activity</router-link>
        <router-link to="/report" class="sidebar-link">📄 Monthly Reports</router-link>
      </aside>

      <main class="main-content">
        <h3>This is your dashboard overview (dummy)</h3>
        <p>You can manage your child's profile, view journaling patterns, and access reports here.</p>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const parentName = ref('Parent') // Dummy name
const router = useRouter()

onMounted(() => {
  // For now, simulate retrieving parent info (e.g., from localStorage or static)
  const storedName = localStorage.getItem('parentName')
  parentName.value = storedName || 'Parent'
})

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', sans-serif;
  background-color: #f0f4f8;
  min-height: 100vh;
  color: #333;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background-color: #2f3e46;
  color: #ffffff;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout-button {
  background-color: #ef476f;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}
.logout-button:hover {
  background-color: #d6325c;
}

.dashboard-body {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 220px;
  background-color: #354f52;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar-link {
  display: block;
  color: #ffffff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}
.sidebar-link:hover {
  background-color: #52796f;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f9fbfc;
}

.welcome {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #51ff97;
}
</style>
