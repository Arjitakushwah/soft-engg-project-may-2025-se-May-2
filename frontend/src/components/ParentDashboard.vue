<template>
  <div class="dashboard-wrapper d-flex min-vh-100">
    <!-- Sidebar -->
    <div class="sidebar bg-light border-end p-4">
      <h4 class="fw-bold mb-4">Hi {{ parentName }}</h4>
      <nav class="nav flex-column">
        <router-link class="nav-link active" to="/add-child">➕ Add Child</router-link>
        <!-- Future links (for layout consistency) -->
        <span class="nav-link text-muted">📅 Calendar Report</span>
        <span class="nav-link text-muted">📓 Journal Analysis</span>
      </nav>
    </div>

    <!-- Main Panel -->
    <div class="main-content flex-fill p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="fw-bold">Parent’s Dashboard</h3>
        <button @click="logout" class="btn btn-outline-danger">Logout</button>
      </div>

      <!-- Placeholder content -->
      <div class="card shadow-sm p-5 text-center rounded-4">
        <p class="text-muted">Welcome! Select an option from the sidebar to begin.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const parentName = ref('Parent') // Default fallback

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const fetchParentName = async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  try {
    const res = await fetch('http://127.0.0.1:5000/api/parent-name', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    if (res.ok) parentName.value = data.name
  } catch {
    router.push('/login')
  }
}

onMounted(fetchParentName)
</script>

<style scoped>
.dashboard-wrapper {
  font-family: 'Comic Neue', cursive;
  background: linear-gradient(135deg, #fff8dc, #e0f7fa);
}

.sidebar {
  width: 250px;
  background-color: #fffaf0;
  font-family: 'Fredoka One', cursive;
}

.nav-link {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.1rem;
  cursor: pointer;
}

.nav-link.active {
  color: #ff6a88;
  font-weight: bold;
}

.nav-link:hover {
  text-decoration: underline;
}

.main-content {
  background-color: #f9f9f9;
}

.card {
  background: #ffffff;
  border: none;
}
</style>
