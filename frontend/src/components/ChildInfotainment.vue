<template>
  <div class="wrapper">
    <div class="search-container">
      <input type="text" placeholder="Search your topic here" v-model="searchText" />
      <button @click="performSearch">Search</button>
    </div>
    <h3 class="section-title">Explore Topics</h3>
    <div class="topic-list">
      <div class="topic-card" v-for="(desc, topic) in topicData" :key="topic" @click="goToResult(topic)">
        {{ topic }}
      </div>
    </div>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const searchText = ref('')
const errorMessage = ref('')

const topicData = {
  Maths: 'Matrix multiplication breakthrough algorithm.',
  Science: 'Europa’s water plumes hint at life.',
  Animal: 'New giant trapdoor spider species in Australia.'
}

function performSearch() {
  const trimmed = searchText.value.trim()
  if (!trimmed) {
    errorMessage.value = 'Please enter a topic to search.'
    return
  }

  errorMessage.value = ''
  router.push({ name: 'Result', params: { topic: trimmed } })
}

function goToResult(topic) {
  router.push({ name: 'Result', params: { topic } })
}
</script>

<style scoped>
.wrapper {
  max-width: 800px;
  margin: 30px auto;
  padding: 1rem;
  font-family: 'Segoe UI', sans-serif;
}

.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input[type='text'] {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  padding: 10px 20px;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background-color: #2a52b9;
}

.section-title {
  text-align: center;
  font-size: 20px;
  margin-bottom: 10px;
  color: #1e3a8a;
}

.topic-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
}

.topic-card {
  background-color: #f0f4ff;
  padding: 15px 25px;
  border-radius: 8px;
  border-left: 6px solid #1e3a8a;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.topic-card:hover {
  background-color: #e2ebff;
  transform: scale(1.02);
}

.error-message {
  color: red;
  margin-top: 15px;
  font-weight: bold;
  text-align: center;
}
</style>