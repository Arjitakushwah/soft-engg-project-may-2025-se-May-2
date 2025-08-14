<template>
  <div class="page-wrapper">
    <div class="app-header"> 
      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="70" fill="#756bdb" class="bi bi-tv" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M2.5 13.5A.5.5 0 0 1 3 13h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zM13.991 3H2c-.325 0-.502.078-.602.145a.758.758 0 0 0-.254.302A1.46 1.46 0 0 0 1 4.01V10c0 .325.078.502.145.602.07.105.17.188.302.254a1.464 1.464 0 0 0 .538.143L2.01 11H14c.325 0 .502-.078.602-.145a.758.758 0 0 0 .254-.302 1.464 1.464 0 0 0 .143-.538L15 9.99V4c0-.325-.078-.502-.145-.602a.757.757 0 0 0-.302-.254A1.46 1.46 0 0 0 13.99 3zM14 2H2C0 2 0 4 0 4v6c0 2 2 2 2 2h12c2 0 2-2 2-2V4c0-2-2-2-2-2z"/>
      </svg>
      <h1>Buzz of Knowledge</h1>
    </div> 
    
    
    <!-- Search Past News -->
    <div class="search-bar">
      <input class="search" type="text" v-model="searchQuery" placeholder="Search your past news..." />
      <button @click="searchNews" class="search-btn">Search</button>
    </div>

    <!-- Predefined Topics -->
    <div class="predefined-topics">
      <h2 class="section-title">Explore Topics</h2>
      <div class="topics-grid">
        <div 
          v-for="topic in dailyTopics" 
          :key="topic.name" 
          class="topic-card"
          @click="goToTopic(topic.name)"
        >
          <i :class="topic.icon" class="topic-icon"></i>
          <div class="topic-name">{{ topic.name }}</div>
        </div>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'; // Import 'computed'
import { useRouter } from 'vue-router';

const router = useRouter();
const searchQuery = ref('');
const errorMessage = ref('');

// 1. Create a master list with all your topics (current + new ones).
const allTopics = [
  { name: 'Science', icon: 'bi bi-lightbulb' },
  { name: 'Technology', icon: 'bi bi-cpu' },
  { name: 'Sports', icon: 'bi bi-trophy' },
  { name: 'Health', icon: 'bi bi-heart-pulse' },
  { name: 'Education', icon: 'bi bi-book' },
  { name: 'Environment', icon: 'bi bi-tree' },
  { name: 'History', icon: 'bi bi-hourglass-split' },
  { name: 'Entertainment', icon: 'bi bi-film' },
  { name: 'Space', icon: 'bi bi-stars' },
  { name: 'Animals', icon: 'bi bi-bug-fill' },
  { name: 'Art', icon: 'bi bi-palette' },
  { name: 'Music', icon: 'bi bi-music-note-beamed' },
  { name: 'Geography', icon: 'bi bi-globe-americas' },
  { name: 'Inventions', icon: 'bi bi-tools' },
  { name: 'Mythology', icon: 'bi bi-shield-shaded' },
  { name: 'Cooking', icon: 'bi bi-egg-fried' },
];

// 2. Create a computed property to get the daily topics.
const dailyTopics = computed(() => {
  const topicsToShow = 15; // How many topics to show at once.
  const now = new Date();
  const startOfYear = new Date(now.getFullYear(), 0, 0);
  const diff = now - startOfYear;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay); // A number from 1 to 365.

  // Calculate the starting index based on the day of the year.
  // The '%' (modulo) operator ensures the index wraps around.
  const startIndex = dayOfYear % allTopics.length;

  // Create an array that's double the master list to easily handle wrapping.
  const rotatedTopics = [...allTopics, ...allTopics];

  // Slice the required number of topics from the calculated start index.
  return rotatedTopics.slice(startIndex, startIndex + topicsToShow);
});

function searchNews() {
  if (!searchQuery.value.trim()) return;
  router.push({ name: "infoResult", query: { search: searchQuery.value.trim() } });
}

function goToTopic(topic) {
  router.push({ name: 'infoResult', query: { topic } });
}
</script>

<style scoped>
.page-wrapper {
  max-width: 950px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: 'Poppins', sans-serif;
}

.app-header { 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 1rem; 
  margin-bottom: 2rem; 
  color: #756bdb; 
} 

.app-header h1 { 
  font-family: 'Fredoka One', cursive; 
  font-size: 2rem; 
  margin: 0; 
} 


.search-bar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.search:focus {
  border: 2px solid;
  outline: none;
  border-color: #756bdb;
}

.search-bar input {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.search-btn {
  padding: 0.75rem 1.25rem;
  background: #756bdb;
  color: #F7D96f;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}


.predefined-topics {
  margin-bottom: 2rem;
}
.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #34495e;
}
.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}
.topic-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.topic-card:hover {
  background: #f0f9ff;
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.25);
}
.topic-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  color: #756bdb;
}
.topic-name {
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 600;
}
.error-message {
  text-align: center;
  color: red;
  font-weight: bold;
  margin-top: 1rem;
}
</style>
