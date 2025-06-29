<template>
  <section>
    <div class="cards-grid">
      <div class="card name-card">
        <h3>Profile</h3>
        <p><strong>Name:</strong> {{ childName }}</p>
      </div>
      <div class="card number-card">
        <h3>Streak</h3>
        <p class="number">5</p>
      </div>
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
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const childName = ref('Child')
onMounted(() => {
  const storedName = localStorage.getItem('username')
  childName.value = storedName || 'Child'
})
</script>

<style scoped>
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background-color: #f5f5f5;
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