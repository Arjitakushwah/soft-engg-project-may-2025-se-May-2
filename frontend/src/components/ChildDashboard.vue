<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="branding">
        <h2 class="greeting">Hi, <span class="username">{{ childName }}</span></h2>
        </div>
        <p class="greeting">Welcome to your Dashboard</p>
      
      <button @click="logout" class="logout-button">Logout</button>
    </header>

    <main class="main-content">
      <!-- Future content can be added here -->
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const childName = ref('Child')
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/child_dashboard', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const data = await res.json()
  if (res.ok) {
    childName.value = data.username || data.name
  } else {
    childName.value = 'Child'
  }
})

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', sans-serif;
  background-color: #f6f9fc;
  min-height: 100vh;
  color: #333;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background-color: #1e1e2f;
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.branding {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.greeting {
  font-size: 1.6rem;
  margin: 0;
}

.username {
  color: #00f7ff;
}

.subtitle {
  font-size: 1rem;
  color: #cbd5e1;
}

.logout-button {
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
.logout-button:hover {
  background-color: #e63946;
}

.main-content {
  padding: 2rem;
}
</style>
