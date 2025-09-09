<template>
  <div class="journal-container">
    <div class="journal-header">
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="70" fill="#756bdb" class="bi bi-journal-text" viewBox="0 0 16 16">
          <path d="M5 10.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
          <path d="M3 0h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-1h1v1a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1H1V2a2 2 0 0 1 2-2"/>
          <path d="M1 5v-.5a.5.5 0 0 1 1 0V5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0V8h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0v.5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1z"/>
        </svg>
        <h1>Footprints of My Day</h1>
    </div>

    <div class="search-container">

      <div class="date-picker-wrapper">
        <button @click="showCalendar = !showCalendar" class="date-picker-btn">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/><line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/><line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/><line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/></svg>
          <span>{{ selectedDateForSearch ? formatDate(selectedDateForSearch) : 'Select Date' }}</span>
        </button>
        <transition name="fade">
          <div v-if="showCalendar" class="calendar-modal">
            <div class="calendar-header">
              <button @click="previousMonth">&lt;</button>
              <span>{{ currentMonthYear }}</span>
              <button @click="nextMonth">&gt;</button>
            </div>
            <div class="calendar-grid">
              <div v-for="day in daysInMonth" :key="day.date" 
                   :class="['calendar-day', { 'is-today': day.isToday, 'is-selected': day.date === selectedDateForSearch, 'is-other-month': !day.isCurrentMonth }]"
                   @click="selectDate(day)">
                {{ day.day }}
              </div>
            </div>
          </div>
        </transition>
      </div>
      
      <div class="mood-select">
        <svg class="mood-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 14s1.5 2 4 2 4-2 4-2" fill="none" stroke="currentColor" stroke-width="2"/><line x1="9" y1="9" x2="9.01" y2="9" stroke="currentColor" stroke-width="2"/><line x1="15" y1="9" x2="15.01" y2="9" stroke="currentColor" stroke-width="2"/></svg>
        <select v-model="search_Mood">
          <option value="">All Moods</option>
          <option v-for="mood in validMoods" :key="mood" :value="mood">{{ mood }}</option>
        </select>
      </div>
      
      <button @click="performSearch" class="search-btn" :disabled="isSearching">
        <svg v-if="!isSearching" class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" fill="none" stroke="currentColor" stroke-width="2"/></svg>
        <svg v-else class="spinner" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10" fill="none" stroke="currentColor" stroke-width="2"><animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/></path></svg>
        {{ isSearching ? 'Searching...' : 'Search' }}
      </button>
    </div>

    <form @submit.prevent="submitJournal" class="journal-form">
      <div class="text-container">
        <label for="message">
          <svg class="label-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.375 2.625a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4Z"/></svg>
          Write about your day:
        </label>
        <textarea
          id="message"
          v-model="journalText"
          placeholder="What happened today? How are you feeling?"
          required
        ></textarea>
      </div>

      <button type="submit" :disabled="loading" class="submit-btn">
        <svg v-if="!loading" class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7Z" fill="none" stroke="currentColor" stroke-width="2"/></svg>
        <svg v-else class="spinner" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10" fill="none" stroke="currentColor" stroke-width="2"><animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/></path></svg>
        {{ loading ? 'Submitting...' : 'Save Journal' }}
      </button>
    </form>

    <div v-if="submitted" class="mood-result" :class="detectedMood">
      <div class="mood-icon-container">
        <svg v-if="detectedMood === 'happy'" class="result-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 14s1.5 2 4 2 4-2 4-2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 9h.01M15 9h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <svg v-else-if="detectedMood === 'sad'" class="result-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16s-1.5-2-4-2-4 2-4 2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 9h.01M15 9h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <svg v-else class="result-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><line x1="8" y1="15" x2="16" y2="15" stroke="currentColor" stroke-width="2"/><path d="M9 9h.01M15 9h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </div>
      <div class="mood-text">
        <h3>Detected Mood: <span>{{ detectedMood }}</span></h3>
        <p>{{ statusMessage }}</p>
      </div>
    </div>

    <div v-if="searchResults.length" class="results-section">
      <h3 class="results-header">
        <svg class="results-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2"/><line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2"/><polyline points="10 9 9 9 8 9"/></svg>
        Search Results
      </h3>
      <div v-for="entry in searchResults" :key="entry.id" class="result-card" :class="entry.mood">
        <div class="result-header">
          <div class="date-container">
            <svg class="date-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/><line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/><line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/><line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/></svg>
            <span class="date">{{ formatDate(entry.date) }}</span>
            <span class="time">{{ formatTime(entry.created_at) }}</span>
          </div>
          <div class="mood-tag" :class="entry.mood">
            <span>{{ entry.mood }}</span>
          </div>
        </div>
        <p class="journal-text">{{ entry.text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const search_Mood = ref('')
const journalText = ref('')
const loading = ref(false)
const isSearching = ref(false)
const submitted = ref(false)
const detectedMood = ref('')
const statusMessage = ref('')
const searchResults = ref([])

const validMoods = [
    "happy", "sad", "angry", "excited", "depressed", "anxious",
    "lonely", "frustrated", "tired", "joyful", "scared", "worried",
    "upset", "relaxed", "stressed", "bored", "hopeful", "grateful",
    "neutral", "proud", "embarrassed", "nostalgic", "apathetic", "disappointed", "sarcastic"
];

const showCalendar = ref(false);
const calendarDate = ref(new Date());
const selectedDateForSearch = ref('');

const currentMonthYear = computed(() => {
    return calendarDate.value.toLocaleDateString(undefined, { year: 'numeric', month: 'long' });
});

const daysInMonth = computed(() => {
    const date = new Date(calendarDate.value);
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const days = [];
    
    const todayDate = new Date();
    const todayString = `${todayDate.getFullYear()}-${String(todayDate.getMonth() + 1).padStart(2, '0')}-${String(todayDate.getDate()).padStart(2, '0')}`;
    const startDayOfWeek = firstDay.getDay();
    for (let i = 0; i < startDayOfWeek; i++) {
        const prevMonthDay = new Date(year, month, 0);
        prevMonthDay.setDate(prevMonthDay.getDate() - i);
        days.unshift({ day: prevMonthDay.getDate(), date: null, isCurrentMonth: false });
    }

    for (let i = 1; i <= lastDay.getDate(); i++) {
        const y = year;
        const m = String(month + 1).padStart(2, '0');
        const d = String(i).padStart(2, '0');
        const dateString = `${y}-${m}-${d}`;
        
        days.push({
            day: i,
            date: dateString,
            isCurrentMonth: true,
            isToday: dateString === todayString
        });
    }
    return days;
});

function previousMonth() {
    calendarDate.value = new Date(calendarDate.value.setMonth(calendarDate.value.getMonth() - 1));
}

function nextMonth() {
    calendarDate.value = new Date(calendarDate.value.setMonth(calendarDate.value.getMonth() + 1));
}

function selectDate(day) {
    if (day.isCurrentMonth) {
        selectedDateForSearch.value = day.date;
        showCalendar.value = false;
    }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const [year, month, day] = dateString.split('-');
  const date = new Date(year, month - 1, day);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return date.toLocaleDateString(undefined, options);
}

const formatTime = (timeString) => {
  if (!timeString) return ''
  
  const [hours, minutes] = timeString.split(':');
  const date = new Date();
  date.setHours(hours, minutes);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const performSearch = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return alert('You are not logged in.')

  isSearching.value = true;
  const params = new URLSearchParams()
  if (selectedDateForSearch.value) params.append('date', selectedDateForSearch.value)
  if (search_Mood.value) params.append('mood', search_Mood.value)

  try {
    const res = await fetch(`https://slice-abcd.onrender.com/journal/search?${params}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const data = await res.json()
    if (!res.ok) return alert(data.error || 'Search failed.')

    searchResults.value = data.entries || []
  } catch (err) {
    console.error(err)
    alert('Search error')
  } finally {
      isSearching.value = false;
  }
}

const submitJournal = async () => {
  if (!journalText.value.trim()) return alert('Please write something.')

  const token = localStorage.getItem('access_token')
  if (!token) return alert('You must be logged in.')

  loading.value = true
  try {
    const res = await fetch('https://slice-abcd.onrender.com/journal', {
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
  } catch (error) {
    console.error(error)
    alert('Something went wrong.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Fredoka+One&display=swap');

.journal-container {
  font-family: 'Comic Neue', cursive;
  width: 90%;
  max-width: 1000px;
  margin: 1.5rem auto;
  background: #F8F8FF;
  border-radius: 12px;
}

.journal-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.journal-header h1 {
  font-family: 'Fredoka One', cursive;
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: 1px;
  color: #756bdb;
  text-align: center;
  margin-top: 19px; 
}

.journal-icon {
  width: 40px;
  height: 40px;
  fill: #756bdb;
}


.search-container { 
    margin-top: 20px;
    display: flex; 
    flex-wrap: wrap; 
    gap: 1rem; 
    margin-bottom: 1.5rem; 
    align-items: center; 
    justify-content: center; 
  }

.date-picker-wrapper { position: relative; flex: 1; min-width: 200px; }
.mood-select { flex: 1; min-width: 200px; position: relative;}

.date-picker-btn {
    width: 100%;
    padding: 10px 15px 10px 40px;
    border: 2px solid #e0e7ff;
    border-radius: 8px;
    font-size: 0.95rem;
    background-color: #f8fafc;
    text-align: left;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
}

.date-picker-btn:focus {
  outline: none;
  border-color: #756bdb;
}

.calendar-modal {
    position: absolute;
    top: 100%;
    left: 0;
    width: 300px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10;
    margin-top: 5px;
    padding: 10px;
}

.calendar-header { display: flex; justify-content: space-between; align-items: center; font-weight: bold; padding: 5px; }
.calendar-header button { background: none; border: none; cursor: pointer; font-size: 1.2rem; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; text-align: center; }
.calendar-day { padding: 8px; cursor: pointer; border-radius: 50%; }
.calendar-day:hover { background-color: #f0f0f0; }
.calendar-day.is-other-month { color: #ccc; cursor: default; }
.calendar-day.is-other-month:hover { background-color: transparent; }
.calendar-day.is-today { font-weight: bold; background-color: #e0e7ff; }
.calendar-day.is-selected { background-color: #756bdb; color: white; }

.mood-select select { width: 100%; padding: 10px 15px 10px 40px; border: 2px solid #e0e7ff; border-radius: 8px; font-size: 0.95rem; background-color: #f8fafc; transition: all 0.3s ease; }
.mood-select select:focus { outline: none; border-color: #756bdb; box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2); }
.search-icon, .mood-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; stroke: #64748b; stroke-width: 2; fill: none; }
.search-btn { background-color: #756bdb; color: white; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; font-size: 0.95rem; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: all 0.3s ease; min-width: 120px; }
.search-btn:hover { background-color: #756bdb; transform: translateY(-2px); }
.btn-icon { width: 16px; height: 16px; stroke: currentColor; stroke-width: 2; fill: none; }
.journal-form { background-color: #f8fafc; padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; border: 2px dashed #e0e7ff; }
.text-container { margin-bottom: 1.2rem;}
.text-container label { display: flex; align-items: center; gap: 0.5rem; font-size: 1.1rem; font-weight: bold; color: #334155; margin-bottom: 0.75rem; }
.label-icon { width: 20px; height: 20px; stroke: #756bdb; stroke-width: 2; fill: none; }
textarea { width: 100%; min-height: 150px; padding: 0.75rem; font-size: 0.95rem; border: 2px solid #e0e7ff; border-radius: 8px; resize: vertical; background-color: white; transition: all 0.3s ease; }
textarea:focus { outline: none; border-color: #818cf8; box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2); }
.submit-btn { background-color: #756bdb; color: #ffffff; padding: 10px 20px; border: none; border-radius: 8px; font-weight: bold; font-size: 1rem; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: all 0.3s ease; margin-top: 1rem; width: 100%; justify-content: center; }
.submit-btn:hover { background-color: #756bdb; transform: translateY(-2px); }
.spinner { width: 20px; height: 20px; stroke: white; stroke-width: 2; fill: none; animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.mood-result { display: flex; align-items: center; gap: 1rem; padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 5px solid; }
.mood-result.happy { background-color: #f0fdf4; border-left-color: #10b981; }
.mood-result.sad { background-color: #fef2f2; border-left-color: #ef4444; }
.mood-result.neutral { background-color: #f8fafc; border-left-color: #64748b; }
.mood-icon-container { flex-shrink: 0; }
.result-icon { width: 40px; height: 40px; stroke-width: 2; fill: none; }
.mood-result.happy .result-icon { stroke: #10b981; }
.mood-result.sad .result-icon { stroke: #ef4444; }
.mood-result.neutral .result-icon { stroke: #64748b; }
.mood-text h3 { margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #334155; }
.mood-text h3 span { text-transform: capitalize; }
.mood-text p { margin: 0; color: #64748b; font-size: 0.9rem; }
.results-section { margin-top: 1.5rem; width: 100%; display: flex; flex-direction: column; align-items: center; }
.results-header { display: flex; align-items: center; gap: 0.75rem; color: #756bdb; font-size: 1.25rem; margin-bottom: 1.25rem; padding-bottom: 0.75rem; border-bottom: 2px solid #e0e7ff; width: 80%; max-width: 800px; }
.results-icon { width: 24px; height: 24px; stroke: currentColor; stroke-width: 2; fill: none; }
.result-card { background: white; padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid #e0e7ff; transition: all 0.3s ease; width: 80%; max-width: 800px; }
.result-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }
.result-card.happy { border-left-color: #10b981; }
.result-card.sad { border-left-color: #ef4444; }
.result-card.neutral { border-left-color: #64748b; }
.result-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem; }
.date-container { display: flex; align-items: center; gap: 0.75rem; }
.date-icon { width: 18px; height: 18px; stroke: #64748b; stroke-width: 2; fill: none; }
.date { font-weight: bold; color: #334155; font-size: 1rem; }
.time { color: #64748b; font-size: 0.85rem; }
.mood-tag { display: flex; align-items: center; gap: 0.5rem; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; text-transform: capitalize; }
.mood-tag.happy { background-color: #d1fae5; color: #065f46; }
.mood-tag.sad { background-color: #fee2e2; color: #991b1b; }
.mood-tag.neutral { background-color: #e2e8f0; color: #475569; }
.mood-tag-icon { width: 16px; height: 16px; stroke-width: 2; fill: none; }
.mood-tag.happy .mood-tag-icon { stroke: #065f46; }
.mood-tag.sad .mood-tag-icon { stroke: #991b1b; }
.mood-tag.neutral .mood-tag-icon { stroke: #475569; }
.journal-text { font-size: 1rem; color: #334155; line-height: 1.7; margin: 0; white-space: pre-line; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>