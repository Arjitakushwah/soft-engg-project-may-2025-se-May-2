<template>
  <div class="page-wrapper">
    <h1 class="main-title">Child's News Corner</h1>

    <div class="news-hub">
      <div class="hub-section create-section">
        <input type="text" v-model="promptText" placeholder="Enter a topic to create news" />
        <button @click="generateNews" class="hub-btn create-btn">
          <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10.362 3.292a1.5 1.5 0 00-2.724 0L6.22 6.22l-2.928.42a1.5 1.5 0 00-.832 2.56l2.118 2.064-.5 2.918a1.5 1.5 0 002.176 1.581L10 14.25l2.622 1.379a1.5 1.5 0 002.176-1.581l-.5-2.918 2.118-2.064a1.5 1.5 0 00-.832-2.56l-2.928-.42-1.418-2.928z" />
          </svg>
          Create
        </button>
      </div>

      <div class="divider"></div>

      <div class="hub-section search-section">
        <input type="text" v-model="searchQuery" placeholder="Search your past news..." />
        <button @click="searchNews" class="hub-btn search-btn">
          <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
          </svg>
          Search
        </button>
      </div>
    </div>

    <div class="results-container">
      <div v-if="displayMode === 'welcome'" class="welcome-message">
        <svg class="welcome-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.82h4.82a4.5 4.5 0 00-1.95-1.95l4.3-4.3a1.5 1.5 0 00-2.12-2.12l-4.3 4.3a4.5 4.5 0 00-1.95-1.95v-4.82a6 6 0 017.38-5.84l-2.43 2.43a1.5 1.5 0 002.12 2.12l2.43-2.43zM3.41 2.41a1.5 1.5 0 00-2.12 2.12l5.59 5.59a6.002 6.002 0 01-3.63 7.19v4.82h-1.5a.75.75 0 000 1.5h4.5a.75.75 0 000-1.5h-1.5v-4.82a4.5 4.5 0 001.95-1.95l5.59 5.59a1.5 1.5 0 102.12-2.12L3.41 2.41z" />
        </svg>
        <h2 class="welcome-title">Let's Start a New Adventure!</h2>
        <p class="welcome-subtitle">Create a new article or search your past news</p>
      </div>

      <div v-if="displayMode === 'generated' && generatedCards.length > 0">
        <div class="news-card generated-news" v-for="(news, index) in generatedCards" :key="`gen-${index}`">
          <div class="news-content" v-html="news"></div>
        </div>
        <div class="mark-btn-wrapper">
          <button :disabled="markLoading || markCompleted || waiting" @click="markAsRead" class="mark-btn">
            <span v-if="markCompleted">Completed!</span>
            <span v-else-if="waiting">Wait {{ waitSeconds }}s</span>
            <span v-else-if="markLoading">Marking...</span>
            <span v-else>Mark as Read</span>
          </button>
        </div>
      </div>

      <div v-if="displayMode === 'search' && searchResults.length > 0">
        <div v-for="result in searchResults" :key="`search-${result.id}`" class="news-card found-news">
          <div class="news-meta">
            <strong>{{ new Date(result.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) }}</strong>
          </div>
          <div class="news-content" v-html="result.content"></div>
          <div class="news-status">
            <span v-if="result.is_done" class="status-badge completed">Read</span>
            <span v-else class="status-badge not-done">Not Read Yet</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

  </div>
</template>

<script setup>
import { ref } from 'vue';

// --- STATE MANAGEMENT ---
const promptText = ref('');
const searchQuery = ref('');
const displayMode = ref('welcome'); // Start with the welcome message
const errorMessage = ref('');
const generatedCards = ref([]);
const searchResults = ref([]);
const logId = ref(null);
const markCompleted = ref(false);
const markLoading = ref(false);
const waitSeconds = ref(0);
const waiting = ref(false);

// --- LOGIC FUNCTIONS ---
function splitIntoCards(content) {
  return content.split(/\n\n(?=# )|(?=^### )/gm).filter(Boolean);
}

async function generateNews() {
  if (!promptText.value.trim()) {
    errorMessage.value = 'Please enter a topic to create news.';
    return;
  }
  displayMode.value = 'generated';
  searchResults.value = [];
  errorMessage.value = '';
  generatedCards.value = [];
  markCompleted.value = false;
  waiting.value = false;
  try {
    const token = localStorage.getItem('access_token');
    const res = await fetch('http://localhost:5000/infotainment/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ prompt: promptText.value })
    });
    const data = await res.json();
    if (!res.ok) {
      errorMessage.value = data.error || 'Failed to generate news.';
      return;
    }
    logId.value = data.log_id;
    generatedCards.value = splitIntoCards(data.content);
  } catch (err) {
    errorMessage.value = 'Something went wrong.';
    console.error(err);
  }
}

async function searchNews() {
  if (!searchQuery.value.trim()) {
    errorMessage.value = 'Please enter a search query.';
    return;
  }
  displayMode.value = 'search';
  generatedCards.value = [];
  errorMessage.value = '';
  searchResults.value = [];
  try {
    const token = localStorage.getItem('access_token');
    const query = searchQuery.value.trim();
    const isDate = /^\d{4}-\d{2}-\d{2}$/.test(query);
    const url = isDate
      ? `http://localhost:5000/infotainment/search?date=${encodeURIComponent(query)}`
      : `http://localhost:5000/infotainment/search?q=${encodeURIComponent(query)}`;
    const res = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
    const data = await res.json();
    searchResults.value = data.logs || [];
     if(searchResults.value.length === 0){
      errorMessage.value = "No news found for that search."
    }
  } catch (err) {
    errorMessage.value = 'Search failed.';
    console.error(err);
  }
}

async function markAsRead() {
  if (!logId.value) return;
  markLoading.value = true;
  try {
    const token = localStorage.getItem('access_token');
    const res = await fetch(`http://localhost:5000/infotainment/mark-read/${logId.value}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    if (res.status === 403 && data.wait_seconds) {
      waiting.value = true;
      waitSeconds.value = data.wait_seconds;
      startWaitTimer();
    } else if (res.ok) {
      markCompleted.value = true;
      alert('Marked as read successfully!');
    } else {
      errorMessage.value = data.error || 'Could not mark as read.';
    }
  } catch (err) {
    errorMessage.value = 'Something went wrong.';
    console.error(err);
  } finally {
    markLoading.value = false;
  }
}

function startWaitTimer() {
  const interval = setInterval(() => {
    waitSeconds.value--;
    if (waitSeconds.value <= 0) {
      waiting.value = false;
      clearInterval(interval);
    }
  }, 1000);
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.page-wrapper {
  max-width: 1100px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: 'Poppins', sans-serif;
  background-color: #f0f7ff;
}

.main-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.news-hub {
  display: flex;
  align-items: center;
  background: #ffffff;
  padding: 1rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(41, 128, 185, 0.1);
}

.hub-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1.5rem;
}

.divider {
  width: 2px;
  height: 40px;
  background-color: #e0e6ed;
}

.hub-section input[type='text'] {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #dde4ee;
  border-radius: 12px;
  font-size: 0.95rem;
  font-family: 'Poppins', sans-serif;
  background-color: #f8fafc;
  transition: all 0.2s ease;
}

.hub-section input[type='text']:focus {
  border-color: #3498db;
  outline: none;
  background-color: #fff;
}

.hub-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hub-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-icon {
  width: 1.1rem;
  height: 1.1rem;
}

.create-btn { background-color: #ff6b81; }
.search-btn { background-color: #3498db; }

/* --- Results --- */
.results-container {
  margin-top: 2rem;
}

.welcome-message {
  text-align: center;
  padding: 3rem 2rem;
  background-color: #fff;
  border: 2px dotted #dce9f5;
  border-radius: 20px;
}
.welcome-icon {
  color: #ff6b81;
  width: 3.5rem;
  height: 3.5rem;
  margin-bottom: 1rem;
}
.welcome-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}
.welcome-subtitle {
  font-size: 1rem;
  color: #7f8c8d;
  margin: 0;
}


.news-card {
  padding: 1.5rem;
  margin-top: 1rem;
  border-radius: 16px;
  background-color: #fff;
  border: 1px solid #e0e6ed;
}

.found-news { background-color: #eaf5fc; border-color: #aed6f1; }
.generated-news { background-color: #fff0f1; border-color: #ffcad0; }

.news-meta, .news-status {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #52616b;
}

.news-content {
  white-space: pre-wrap;
  font-size: 1rem;
  line-height: 1.7;
  color: #2c3e50;
}

.mark-btn-wrapper { margin-top: 1.5rem; }
.mark-btn {
  width: 100%;
  padding: 12px;
  background-color: #9b59b6;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
}
.mark-btn:disabled { background-color: #c7a4d6; cursor: not-allowed;}

.error-message {
  text-align: center;
  padding: 1rem;
  margin-top: 1.5rem;
  background-color: #fbebee;
  color: #c0392b;
  border-radius: 12px;
  font-weight: 500;
}


/* Responsive */
@media (max-width: 850px) {
  .news-hub {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  .divider {
    width: 100%;
    height: 2px;
  }
}
</style>