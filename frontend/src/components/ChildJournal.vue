<template>
  <div class="journal-container">
    <div class="search-container">
      <input type="text" placeholder="Search journal by date (e.g. 2024-06-28)" v-model="search_Text" />
      <button @click="performSearch">Search</button>
    </div>
    <div class="emoji-selector">
      <label class="emoji-label">How are you feeling today?</label>
      <div class="emoji-options">
        <span v-for="emoji in emojis" :key="emoji" :class="['emoji', selectedEmoji === emoji ? 'selected' : '']"
          @click="selectEmoji(emoji)">
          {{ emoji }}
        </span>
      </div>
    </div>

    <form @submit.prevent="submitJournal">
      <div class="text-container">
        <label for="message">Write your journal entry:</label><br />
        <textarea id="message" v-model="journalText" placeholder="Reflect on your day..." required></textarea>
      </div>

      <div class="button-container">
        <button type="submit">Submit Journal</button>
      </div>
    </form>
  </div>
</template>
<script setup>
import { ref } from 'vue'

const search_Text = ref('')
const emojis = ['😄', '🙂', '😐', '😢', '😡']
const selectedEmoji = ref('')
const journalText = ref('')

const performSearch = () => {
  console.log('Search for date:', search_Text.value)

}

const selectEmoji = (emoji) => {
  selectedEmoji.value = emoji
  console.log('Selected Emoji:', emoji)
}

const submitJournal = () => {
  if (!selectedEmoji.value) {
    alert('Please select your mood emoji.')
    return
  }

  const journalEntry = {
    date: new Date().toISOString().split('T')[0],
    mood: selectedEmoji.value,
    entry: journalText.value
  }

  console.log('Journal Submitted:', journalEntry)

  // Clear form
  journalText.value = ''
  selectedEmoji.value = ''
  alert('Journal submitted successfully!')
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

.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input[type='text'] {
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

.emoji-selector {
  margin-bottom: 20px;
}

.emoji-label {
  font-size: 16px;
  font-weight: bold;
}

.emoji-options {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.emoji {
  font-size: 30px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.emoji:hover {
  transform: scale(1.2);
}

.selected {
  border: 2px solid #2563eb;
  border-radius: 50%;
  padding: 4px;
  background-color: #e0e7ff;
}

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
</style>