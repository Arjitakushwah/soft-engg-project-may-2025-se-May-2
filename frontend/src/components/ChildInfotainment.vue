<template>
  <div class="wrapper">
    <!-- 🔍 Search Section -->
    <div class="search-box">
      <h3>🔍 Search Saved Stories</h3>
      <input type="text" v-model="searchQuery" placeholder="Search by title or date (e.g., 2025-07-14)" />
      <button @click="searchStories">Search</button>

      <div v-if="searchResults.length > 0" class="results">
        <h4>Search Results</h4>
        <div v-for="result in searchResults" :key="result.id" class="story-card">
          <div class="story-meta">
            <strong>{{ result.date }}</strong> at <em>{{ formatTime(result.marked_at) }}</em>
          </div>
          <div class="story-content" v-html="result.content"></div>
          <div class="story-status">
            <span v-if="result.is_done" class="completed">✅ Read</span>
            <span v-else class="not-done">⏳ Not Read</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 🧠 Generate Section -->
    <div class="generate-box">
      <h3>🧠 Generate New News</h3>
      <input type="text" v-model="promptText" placeholder="Enter your topic of interest" />
      <button @click="generateStory">Generate</button>

      <div v-if="generatedCards.length > 0" class="generated-cards">
        <div class="story-card story-generated" v-for="(story, index) in generatedCards" :key="index">
          <h4>Story {{ index + 1 }}</h4>
          <div class="story-content" v-html="story"></div>
        </div>
        <div class="mark-btn">
          <button :disabled="markLoading || markCompleted || waiting" @click="markAsRead">
            {{ markCompleted ? ' Already Completed' :
               waiting ? `⏳ Wait ${waitSeconds}s` :
               markLoading ? '⏳ Marking...' : ' Mark as Read' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const promptText = ref('')
const errorMessage = ref('')
const searchQuery = ref('')
const generatedCards = ref([])
const searchResults = ref([])
const logId = ref(null)
const markCompleted = ref(false)
const markLoading = ref(false)
const waitSeconds = ref(0)
const waiting = ref(false)

function splitIntoCards(content) {
  return content.split(/\n\n(?=# )|(?=^### )/gm).filter(Boolean)
}

function formatTime(datetimeString) {
  if (!datetimeString) return 'N/A'
  const date = new Date(datetimeString)
  return date.toLocaleTimeString('en-GB')
}

async function generateStory() {
  if (!promptText.value.trim()) {
    errorMessage.value = 'Please enter a prompt.'
    return
  }

  try {
    errorMessage.value = ''
    generatedCards.value = []
    markCompleted.value = false
    waiting.value = false
    waitSeconds.value = 0

    const token = localStorage.getItem('access_token')
    const res = await fetch('http://localhost:5000/infotainment/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ prompt: promptText.value })
    })

    const data = await res.json()
    if (!res.ok) {
      errorMessage.value = data.error || 'Failed to generate story.'
      return
    }

    logId.value = data.log_id
    generatedCards.value = splitIntoCards(data.content)
  } catch (err) {
    errorMessage.value = 'Something went wrong.'
    console.error(err)
  }
}

async function markAsRead() {
  if (!logId.value) return
  markLoading.value = true

  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`http://localhost:5000/infotainment/mark-read/${logId.value}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await res.json()
    if (res.status === 403 && data.wait_seconds) {
      waiting.value = true
      waitSeconds.value = data.wait_seconds
      startWaitTimer()
    } else if (res.ok) {
      markCompleted.value = true
      alert('Marked as read successfully!')
    } else {
      errorMessage.value = data.error || 'Could not mark as read.'
    }
  } catch (err) {
    errorMessage.value = 'Something went wrong.'
    console.error(err)
  } finally {
    markLoading.value = false
  }
}

function startWaitTimer() {
  const interval = setInterval(() => {
    waitSeconds.value--
    if (waitSeconds.value <= 0) {
      waiting.value = false
      clearInterval(interval)
    }
  }, 1000)
}

async function searchStories() {
  if (!searchQuery.value.trim()) return

  try {
    const token = localStorage.getItem('access_token')
    const query = searchQuery.value.trim()
    const isDate = /^\d{4}-\d{2}-\d{2}$/.test(query)

    const url = isDate
      ? `http://localhost:5000/infotainment/search?date=${encodeURIComponent(query)}`
      : `http://localhost:5000/infotainment/search?q=${encodeURIComponent(query)}`

    const res = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await res.json()
    searchResults.value = data.logs || []
  } catch (err) {
    errorMessage.value = 'Search failed.'
    console.error(err)
  }
}
</script>

<style scoped>
.wrapper {
  max-width: 1000px;
  margin: 30px auto;
  padding: 1.5rem;
  font-family: 'Comic Neue', cursive;
  background-color: #fff;
}

.search-box,
.generate-box {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 2px solid #d6e0ff;
  border-radius: 12px;
  background-color: #f3f7ff;
}

input[type='text'] {
  width: 100%;
  padding: 12px;
  margin: 0.8rem 0;
  border: 1px solid #bbb;
  border-radius: 8px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background-color: #2a52b9;
}

.story-card {
  background: #eef4ff;
  padding: 1.2rem;
  margin-top: 1rem;
  border-left: 6px solid #1e3a8a;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.story-generated {
  background-color: #e9fff0;
  border-left-color: #34a853;
}

.story-meta {
  font-size: 14px;
  color: #555;
  margin-bottom: 0.5rem;
}

.story-content {
  white-space: pre-wrap;
  font-size: 15.5px;
  margin-top: 0.4rem;
  color: #222;
}

.story-status {
  margin-top: 0.5rem;
  font-weight: bold;
}

.completed {
  color: green;
}

.not-done {
  color: orange;
}

.mark-btn {
  margin-top: 1.2rem;
  text-align: right;
}

.error-message {
  color: red;
  margin-top: 10px;
  font-weight: bold;
  text-align: center;
}
</style>
