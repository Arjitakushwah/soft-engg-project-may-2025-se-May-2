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
      <div class="cards-grid">
        <!-- Child Name Box -->
        <div class="card name-card">
          <h3>Profile</h3>
          <p><strong>Name:</strong> {{ childName }}</p>
        </div>

        <!-- Number Card -->
        <div class="card number-card">
          <h3>Streak</h3>
          <p class="number">5</p>
        </div>

        <!-- Stars / Badges Card -->
        <div class="card badge-card">
          <h3>Badges Earned</h3>
          <div class="stars">
            <span class="star filled">★</span>
            <span class="star filled">★</span>
            <span class="star filled">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
          </div>
        </div>
      </div>
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

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background-color: #fff;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
}

.name-card h3,
.number-card h3,
.badge-card h3 {
  margin-bottom: 0.8rem;
  color: #333;
}

.number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #0077ff;
}

.stars {
  font-size: 1.8rem;
  color: #f5c518;
}

.star {
  color: #ccc;
}

.star.filled {
  color: #ffc107;
}

</style>