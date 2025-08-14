<template>
  <section class="daily-quote">
    <h1>Daily Motivation</h1>
    <blockquote>{{ quote }}</blockquote>
  </section>
  <Loader v-if="loading" />
  <section class="cards-container">
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

      <div class="card number-card streak-card">
        <h3>Streak</h3>
        <p class="number">{{ currentStreak }}</p>
      </div>

      <div class="card number-card journal-count-card">
        <h3>Journals Written</h3>
        <p class="number">{{ totalJournals }}</p>
      </div>
      
      <div class="card number-card story-reads-card">
        <h3>Stories Read</h3>
        <p class="number">{{ totalStories }}</p>
      </div>

      <div class="card badge-card">
        <h3>🏅 Badges Earned</h3>
        <div class="badge-list">
          <div class="badge" v-for="badge in badges" :key="badge.id">
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
</template>

<script setup>
import { ref, onMounted } from "vue";
import Loader from './Loader.vue';
import { badgeSvgMap, defaultBadgeSvg } from '/src/assets/badges.js';

const childName = ref("Child");
const quote = ref("");
const loading = ref(true);
const currentStreak = ref(0);
const longestStreak = ref(0);
const badges = ref([]);
const totalBadges = ref(0);
const totalJournals = ref(0);
const totalStories = ref(0);
const totalInfotainment = ref(0);


const getBadgeSvg = (badgeName) => {
  return badgeSvgMap[badgeName] || defaultBadgeSvg;
};

const fetchStreakAndBadges = async () => {
  try {
    const res = await fetch("http://localhost:5000/streak-badges", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to fetch streak and badges");

    currentStreak.value = data.current_streak || 0;
    longestStreak.value = data.longest_streak || 0;
    badges.value = data.badges || [];
    totalBadges.value = data.badges_count || 0;
    totalJournals.value = data.total_journals_written || 0;
    totalStories.value = data.total_stories_read || 0;
    totalInfotainment.value = data.total_infotainment_read || 0;
  } catch (err) {
    console.error("Error fetching streak & badges:", err.message);
  }finally {
    loading.value = false;
  }
};

onMounted(() => {
  const storedName = localStorage.getItem("username");
  childName.value = storedName || "Child";

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

  fetchStreakAndBadges();
});
</script>



<style scoped>

.daily-quote {
  width: 100%;
  padding: 1.5rem;
  background: #e9e9e6;
  text-align: center;
  font-family: "Comic Neue", cursive;
  box-sizing: border-box;
  border-radius: 1rem;
  margin-bottom: 2rem;
  font-family: 'Fredoka One', cursive;
  color: #5A4FCF;
}

.daily-quote {
  margin-left: 20px;
  width: 96%;
  color: #5A4FCF;
  font-size: 1.5rem;
  margin-top: 0;
  margin-bottom: 0.75rem;
  margin-bottom: 25px;
}

.daily-quote blockquote {
  font-size: 1rem;
  font-style: italic;
  color: #334155;
  background: #ffffff;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  display: inline-block;
  max-width: 100%;
  margin: 0 auto;
  border-left: 5px solid #5A4FCF;
}

/* Cards Grid Section */
.cards-container {
  padding: 0 1rem;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.card {
  background-color: #898dd9f1;
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.07);
  border: 3px solid #655adb; /* blue border on hover */
}

.card h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
}

.name-card p {
  font-size: 1.1rem;
  color: #475569;
}

.number {
  font-size: 3rem;
  font-weight: bold;
  line-height: 1;
}

.streak-card .number { color: #f9d34a; }
.journal-count-card .number { color: #f9d34a; }
.story-reads-card .number { color: #f9d34a; }

.stars {
  font-size: 1.8rem;
  margin-top: 0.5rem;
}

.star {
  color: #f7f7f7;
}

.star.filled {
  color: #f9d34a;
}

/* Badge Card Specific Styles */
.badge-card {
  grid-column: 1 / -1;
}

.badge-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
  margin-top: 1rem;
}

.badge {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #c6bbcbf1;
  padding: 12px 10px;
  border-radius: 12px;
  font-size: 1rem;
  color: #334155;
  font-weight: 600;
  min-width: 200px;
}

/* ✨ ADDED: Styling for the SVG icon container */
.badge-icon {
  width: 50px;
  height: 50px;
  /* flex-shrink: 1; */
}

.no-badges {
  color: #94a3b8;
  font-size: 1rem;
  margin-top: 0.5rem;
  width: 100%;
}

/* Responsive Adjustments */
@media (max-width: 992px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
  .badge-card {
    grid-column: auto;
  }
}
</style>