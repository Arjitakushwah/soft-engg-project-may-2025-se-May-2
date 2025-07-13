<template>
  <div class="journal-container">
    <!-- Search Section -->
    <div class="search-container">
      <input type="text" placeholder="Search by date (e.g. 2025-07-14)" v-model="search_Text" />
      <select v-model="search_Mood">
        <option value="">All Moods</option>
        <option value="happy">Happy</option>
        <option value="neutral">Neutral</option>
        <option value="sad">Sad</option>
      </select>
      <button @click="performSearch">Search</button>
    </div>

    <!-- Journal Form -->
    <form @submit.prevent="submitJournal">
      <div class="text-container">
        <label for="message">Write your journal entry:</label><br />
        <textarea
          id="message"
          v-model="journalText"
          placeholder="Reflect on your day..."
          required
        ></textarea>
      </div>

      <div class="button-container">
        <button type="submit" :disabled="loading">
          {{ loading ? 'Submitting...' : 'Submit Journal' }}
        </button>
      </div>
    </form>

    <!-- Submission Feedback -->
    <div v-if="submitted" class="mood-result">
      <p><strong>Detected Mood:</strong> {{ detectedMood }}</p>
      <p><strong>Status:</strong> {{ statusMessage }}</p>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults.length" class="results-section">
      <h3>Search Results</h3>
      <div v-for="entry in searchResults" :key="entry.id" class="result-card">
        <div class="result-header">
          <span class="date">{{ entry.date }}</span>
          <span class="time">({{ entry.created_at }})</span>
          <span class="mood-tag" :class="entry.mood">Mood: {{ entry.mood }}</span>
        </div>
        <p class="journal-text">{{ entry.text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const search_Text = ref('')
const search_Mood = ref('')
const journalText = ref('')
const loading = ref(false)
const submitted = ref(false)
const detectedMood = ref('')
const statusMessage = ref('')
const searchResults = ref([])

const performSearch = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return alert('You are not logged in.')

  const params = new URLSearchParams()
  if (search_Text.value) params.append('date', search_Text.value)
  if (search_Mood.value) params.append('mood', search_Mood.value)

  try {
    const res = await fetch(`http://localhost:5000/journal/search?${params}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const data = await res.json()
    if (!res.ok) return alert(data.error || 'Search failed.')

    searchResults.value = data.entries || []
  } catch (err) {
    console.error(err)
    alert('Search error')
  }
}

const submitJournal = async () => {
  if (!journalText.value.trim()) return alert('Please write something.')

  const token = localStorage.getItem('access_token')
  if (!token) return alert('You must be logged in.')

  loading.value = true
  try {
    const res = await fetch('http://localhost:5000/journal', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ text: journalText.value })
    })

    const result = await res.json()
    if (!res.ok) return alert(result.error || 'Submission failed.')

    detectedMood.value = result.mood
    statusMessage.value = result.message
    submitted.value = true
    journalText.value = ''
    alert(`Journal submitted! Mood detected: ${result.mood}`)
  } catch (error) {
    console.error(error)
    alert('Something went wrong.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.journal-container {
  font-family: 'Comic Neue', cursive;
  width: 90%;
  max-width: 900px;
  margin: auto;
  padding: 2rem;
  background: #f9f9fb;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* Search Bar */
.search-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

input[type='text'],
select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}

.search-container button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

/* Form */
.text-container textarea {
  width: 100%;
  height: 140px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  resize: vertical;
  margin-top: 8px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

button[type='submit'] {
  background-color: #10b981;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

button[type='submit']:hover {
  background-color: #0f9c75;
}

/* Submission Feedback */
.mood-result {
  margin-top: 20px;
  padding: 1rem;
  background-color: #e0f7fa;
  border-left: 5px solid #00acc1;
  border-radius: 10px;
}

/* Results Display */
.results-section {
  background-color: #f0f8ff;
  padding: 1rem;
  border-radius: 10px;
  margin-top: 1.5rem;
}

.result-card {
  background: white;
  border-left: 4px solid #3b82f6;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.result-header {
  display: flex;
  gap: 1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.date {
  color: #2563eb;
}

.time {
  color: #555;
  font-size: 0.9rem;
}

.mood-tag {
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 0.9rem;
  text-transform: capitalize;
}

.mood-tag.happy {
  background-color: #d1fae5;
  color: #059669;
}

.mood-tag.sad {
  background-color: #fee2e2;
  color: #b91c1c;
}

.mood-tag.neutral {
  background-color: #f3f4f6;
  color: #4b5563;
}

.journal-text {
  font-size: 1rem;
  color: #333;
  line-height: 1.5;
}
</style>
  