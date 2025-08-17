<template>
  <div class="dashboard-container">
    <section class="daily-quote">
      <h1>Daily Motivation</h1>
      <blockquote>{{ quote }}</blockquote>
    </section>
    
    <Loader v-if="loading" />
    
    <section class="cards-container" v-else>
      <div class="cards-grid">
        <div class="card profile-card">
            <img :src="`https://placehold.co/80x80/a29cdf/ffffff?text=${childName.charAt(0).toUpperCase()}`" 
                 onerror="this.src='https://placehold.co/80x80/ccc/ffffff?text=?'"
                 alt="Avatar" 
                 class="avatar">
            <div class="profile-info">
              <h3>{{ childName }}</h3>
              <div class="profile-details">
                <div class="detail-item">
                  <span class="detail-label">Age</span>
                  <span class="detail-value">{{ childAge }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Best Streak</span>
                  <span class="detail-value">{{ longestStreak }} days</span>
                </div>
              </div>
            </div>
        </div>

        <div class="card number-card streak-card">
          <div class="card-content">
            <i class="bi bi-fire card-icon"></i>
            <p class="number">{{ currentStreak }}</p>
            <h3>Day Streak</h3>
          </div>
        </div>

        <div class="card number-card journal-count-card">
          <div class="card-content">
            <i class="bi bi-journal-richtext card-icon"></i>
            <p class="number">{{ totalJournals }}</p>
            <h3>Journals</h3>
          </div>
        </div>
        
        <div class="card number-card story-reads-card">
          <div class="card-content">
            <i class="bi bi-book-half card-icon"></i>
            <p class="number">{{ totalStories }}</p>
            <h3>Stories Read</h3>
          </div>
        </div>

        <div class="card badge-card">
          <h3>🏅 Badges Earned</h3>
          <div class="badge-list">
            <div class="badge" v-for="badge in badges" :key="badge.name">
              <span class="badge-icon" v-html="getBadgeSvg(badge.name)"></span>
              <span class="label">{{ badge.name }}</span>
            </div>
            <div v-if="badges.length === 0" class="no-badges">
              No badges yet. Start your first quest!
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Loader from './Loader.vue';
import { badgeSvgMap, defaultBadgeSvg } from '/src/assets/badges.js';

const childName = ref("Child");
const childAge = ref(0);
const quote = ref("");
const loading = ref(true);
const currentStreak = ref(0);
const longestStreak = ref(0);
const badges = ref([]);
const totalJournals = ref(0);
const totalStories = ref(0);

const getBadgeSvg = (badgeName) => {
  return badgeSvgMap[badgeName] || defaultBadgeSvg;
};

const apiRequest = async (url) => {
    const token = localStorage.getItem("access_token");
    if (!token) {

        console.error("No auth token found");
        return;
    }
    const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.error || `Failed to fetch data from ${url}`);
    }
    return data;
};

const fetchDashboardData = async () => {
    loading.value = true;
    try {
        const [profileData, streakData] = await Promise.all([
            apiRequest("http://localhost:5000/child_dashboard"),
            apiRequest("http://localhost:5000/streak-badges")
        ]);
        if (profileData) {
            childName.value = profileData.name || "Child";
            childAge.value = profileData.age || 0;
        }

        if (streakData) {
            currentStreak.value = streakData.current_streak || 0;
            longestStreak.value = streakData.longest_streak || 0;
            badges.value = streakData.badges || [];
            totalJournals.value = streakData.total_journals_written || 0;
            totalStories.value = streakData.total_stories_read || 0;
        }

    } catch (err) {
        console.error("Error fetching dashboard data:", err.message);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
  const quotes = [
    "Believe in yourself and all that you are!",
    "Every day is a chance to learn something new.",
    "You are braver than you believe and smarter than you think.",
    "Mistakes help you grow. Keep going!",
    "Great things take time. Stay curious!",
    "A little progress each day adds up to big results.",
    "Be the reason someone smiles today!",
    "Your imagination is your superpower.",
    "Kindness makes everything better.",
    "Ask questions. Discover new things.",
    "You are capable of amazing things.",
    "Today is a brand new adventure.",
    "Let your creativity shine bright.",
    "Every pro was once a beginner.",
    "Do your best today!",
    "Your smile is a gift to the world.",
    "A book is an adventure waiting to be opened.",
    "Small steps lead to big journeys.",
    "Be curious. Be kind. Be you.",
    "The more you learn, the more you grow.",
    "Challenges are chances to be awesome.",
    "It's a great day to have a great day!"
  ];
  quote.value = quotes[Math.floor(Math.random() * quotes.length)];

  fetchDashboardData();
});
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.dashboard-container {
  padding: 1rem 2rem;
  background-color: #f7f8fc;
  min-height: 100vh;
}

.daily-quote {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  text-align: center;
  border-radius: 1rem;
  margin-bottom: 2rem;
  color: #ffffff;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
}

.daily-quote h1 {
  font-family: 'Fredoka One', cursive;
  font-size: 1.5rem;
  margin: 0 0 0.75rem 0;
  opacity: 0.9;
}

.daily-quote blockquote {
  font-size: 1.1rem;
  font-style: italic;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 8px;
  display: inline-block;
  margin: 0 auto;
  border-left: 4px solid #fff;
}

.cards-container {
  padding: 0 1rem;
}

.cards-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
}

.card {
  background-color: #ffffff;
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-size: 1.1rem;
  font-weight: 600;
}

.profile-card {
  background: #fff;
  display: flex;
  align-items: center;
  text-align: center;
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
 
  object-fit: cover;
  border: 4px solid #a29cdf;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  align-content: center;
  align-items: center;
}
.profile-info {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.profile-info h3 {
  margin: 0 0 0.75rem 0;
  font-size: 2rem;
  color: #2d3748;
}
.profile-details {
    display: flex;
    gap: 1rem;
    margin-top: 0;
}
.detail-item {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: linear-gradient(145deg, #f9faff, #eef2ff);
    padding: 0.75rem;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #e2e8f0;
}
.detail-label {
    font-size: 0.8rem;
    color: #718096;
    font-weight: 600;
    margin-bottom: 0.25rem;
}
.detail-value {
    font-size: 1.4rem;
    color: #4a5568;
    font-weight: 700;
    line-height: 1.2;
}


.number-card .card-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}
.card-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}
.number {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.5rem;
}
.streak-card { background:  #fceabb; color: #9c6c00; }
.journal-count-card { background: #f8ceec; color: #5e4c8c; }
.story-reads-card { background: #a8e063; color: #2e5c19; }

.streak-card .card-icon, .streak-card h3 { color: #c08600; }
.journal-count-card .card-icon, .journal-count-card h3 { color: #6f5aa8; }
.story-reads-card .card-icon, .story-reads-card h3 { color: #386e21; }

.badge-card {
  grid-column: 1 / -1;
}
.badge-card h3 {
    font-size: 1.5rem;
    color: #2d3748;
}
.badge-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}
.badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: #f7f8fc;
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  color: #4a5568;
  font-weight: 600;
  width: 120px;
  border: 1px solid #e2e8f0;
}
.badge-icon {
  width: 50px;
  height: 50px;
}
.no-badges {
  color: #a0aec0;
  font-size: 1rem;
  margin-top: 0.5rem;
  width: 100%;
}

@media (min-width: 768px) {
    .cards-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1200px) {
    .cards-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
</style>
