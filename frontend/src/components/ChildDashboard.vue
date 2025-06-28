<template>
  <div class="dashboard-container">
    <h2 class="welcome">Welcome Child Dashboard </h2>
    <main class="main-content">
      <div class="cards-grid">
        <!-- Child Name Box -->
        <div class="card name-card">
          <h3>Profile</h3>
          <p><strong>Name:</strong> {{ childName }}</p>
        </div>

        <!-- Streak Card -->
        <div class="card number-card">
          <h3>Streak</h3>
          <p class="number">5</p>
        </div>

        <!-- Badges Card -->
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

const router = useRouter()
const childName = ref('Child')

// Role-based protection
onMounted(() => {
  const role = localStorage.getItem('role')
  const name = localStorage.getItem('name')

  if (role !== 'child') {
    router.push('/login')
  }

  childName.value = name || 'Child'

  // Optional: API fetch logic if backend is restored
  /*
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/child_dashboard', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const data = await res.json()
  if (res.ok) {
    childName.value = data.username || data.name
  }
  */
})
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', sans-serif;
  background-color: white;
  min-height: 100vh;
  color: #333;
  display: flex;
  flex-direction: column;
}

.welcome {
  background-color: #f3f6fb; /* very light shade from image */
  padding: 1.2rem 3rem;
  font-size: 1.8rem;
  font-weight: 600;
  color: #000000;
  border-bottom: 1px solid #dee2e6; /* optional */
}


.main-content {
  padding: 2rem;
  background-color: #ffffff;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background-color:#f5f5f5;
  border-radius: 1rem;
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
