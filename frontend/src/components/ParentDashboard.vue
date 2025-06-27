<template>
  <div class="dashboard-container">
      <h2 class="welcome">Welcome to your Parent Dashboard </h2>
    <div class="dashboard-body">
      <aside class="sidebar">
        <router-link to="/add-child" class="sidebar-link">➕ Add Child</router-link>
      </aside>


    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const parentName = ref('')
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/parent_dashboard', {
    headers: { Authorization: `Bearer ${token}` }
  })
  const data = await res.json()
  parentName.value = res.ok ? data.name || data.username : 'Parent'
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

.dashboard-body {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 200px;
  background-color: #354f52;
  padding: 1.5rem 1rem;
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

.action-button {
  display: inline-block;
  background-color: #457b9d;
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.3s;
}
.action-button:hover {
  background-color: #1d3557;
}
</style>
