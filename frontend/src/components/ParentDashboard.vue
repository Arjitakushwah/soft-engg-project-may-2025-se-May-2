<template>
  <div class="dashboard-container">
    <h2 class="welcome">Welcome Parent Dashboard </h2>

    <div class="dashboard-body">
      <aside class="sidebar">
        <router-link to="/add-child" class="sidebar-link">➕ Add Child</router-link>
      </aside>

      <main class="main-content">
        <h3>Manage Your Child's Progress and Activities</h3>
        <p>Use the sidebar to add a child, view reports, or assign tasks.</p>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const parentName = ref('Parent')
const router = useRouter()

onMounted(() => {
  const role = localStorage.getItem('role')
  const name = localStorage.getItem('name')

  if (role !== 'parent') {
    router.push('/login')
  } else {
    parentName.value = name || 'Parent'
  }

  // Optional: Fetch from backend if needed later
  /*
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/parent_dashboard', {
    headers: { Authorization: `Bearer ${token}` }
  })
  const data = await res.json()
  parentName.value = res.ok ? data.name || data.username : 'Parent'
  */
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

.welcome {
  font-size: 1.8rem;
  margin: 1.5rem;
  color: black;
}

.dashboard-body {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 200px;
  background-color: #354f52;
  padding: 1.5rem 1rem;
  min-height: calc(100vh - 5rem);
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
</style>
