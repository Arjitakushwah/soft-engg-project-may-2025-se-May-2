<template>
  <section class="daily-quote">
    <h3>Daily Motivation</h3>
    <blockquote>{{ quote }}</blockquote>
  </section>

  <section>
    <div class="cards-grid">
      <div class="card name-card">
        <h3>Profile</h3>
        <p><strong>Name:</strong> {{ childName }}</p>
        <div class="stars">
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star">★</span>
          <span class="star">★</span>
        </div>
      </div>
      <div class="card number-card">
        <h3>Streak</h3>
        <p class="number">5</p>
      </div>
      <!-- <div class="card badge-card">
        <h3>Badges Earned</h3>
        <div class="stars">
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star">★</span>
          <span class="star">★</span>
        </div>
      </div> -->

      <!-- Total Journals -->
      <div class="card journal-count-card">
        <h3>Journals Written</h3>
        <p class="number">{{ totalJournals }}</p>
      </div>
    </div>
    <!-- Badges Earned -->
<div class="card badge-card">
  <h3>🏅 Badges Earned</h3>
  <div class="badge-list">
    <div class="badge" v-for="badge in badges" :key="badge.id">
      <span class="emoji">{{ badge.icon }}</span>
      <span class="label">{{ badge.name }}</span>
    </div>
    <div v-if="badges.length === 0" class="no-badges">No badges yet. Start your first quest!</div>
  </div>
</div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const childName = ref('Child')
const quote = ref('')
const totalJournals = ref(12)

const badges = ref([
  { id: 1, name: 'First Journal', icon: '📝' },
  { id: 2, name: 'Story Explorer', icon: '📖' },
  { id: 3, name: '3-Day Streak', icon: '🔥' }
])


onMounted(() => {
  const storedName = localStorage.getItem('username')
  childName.value = storedName || 'Child'

  const quotes = [
    "Believe in yourself and all that you are!",
    "Every day is a chance to learn something new.",
    "You are braver than you believe and smarter than you think.",
    "Mistakes help you grow. Keep going!",
    "Great things take time. Stay curious!",
    "A little progress each day adds up to big results.",
    "Be the reason someone smiles today!"
  ]

  quote.value = quotes[Math.floor(Math.random() * quotes.length)]
})
</script>

<style scoped>

.daily-quote {
  width: 100%;
  padding: 2rem 1rem;
  background: #e0f2fe;
  text-align: center;
  font-family: 'Comic Neue', cursive;
  box-sizing: border-box;
  border-radius: 1rem;
}

.daily-quote h3 {
  color: #3b82f6;
  font-size: 1.6rem;
  margin-bottom: 0.79rem;
}

.daily-quote blockquote {
  font-size: 1.3rem;
  font-style: italic;
  color: #333;
  background: #f0f8ff;
  
  padding: 1rem 1.5rem;
  border-radius: 8px;
  display: inline-block;
  max-width: 100%;
  margin: 0 auto;
}

/* Cards Grid Section */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  padding: 2rem 1rem;
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

.badge-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
  margin-top: 1rem;
}

.badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff8f0;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #444;
  border: 1px solid #ffd1a9;
  font-weight: 500;
}

.emoji {
  font-size: 1.2rem;
}

.no-badges {
  color: #aaa;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

</style>
