<template>
  <div class="card">
    <h4>{{ topic }}</h4>
    <p v-if="info">{{ info }}</p>
    <p v-else>No data found for "{{ topic }}"</p>
    <div class="button-container">
      <button class="secondary-btn" @click="goBack">Back</button>
      <button class="primary-btn" @click="markAsRead">Mark as Read</button>
    </div>
    <p v-if="message" class="read-message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const topic = route.params.topic
const message = ref('')

const search_Results = {
  Maths: 'Mathematicians develop a new algorithm reducing matrix multiplication time, breaking a 50-year-old record.',
  Science: 'NASA confirms evidence of water vapor plumes on Europa, a key sign in the search for extraterrestrial life.',
  Animal: 'A new species of giant trapdoor spider discovered in Australia, highlighting biodiversity in remote habitats.'
}

const info = ref(search_Results[topic] || '')

function goBack() {
  router.back()
}

function markAsRead() {
  message.value = `Marked "${topic}" as read.`

}
</script>
<style scoped>
.card {
  max-width: 90%;
  margin: 40px auto;
  padding: 24px;
  background: linear-gradient #fceabb;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', sans-serif;
  color: #2c3e50;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.01);
}

.card h4 {
  margin-bottom: 12px;
  font-size: 24px;
  color: #1a1a1a;
  font-weight: bold;
}

.card p {
  font-size: 17px;
  color: #333;
  line-height: 1.5;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.primary-btn,
.secondary-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 15px;
}

.primary-btn {
  background-color: #1e3a8a;
  color: white;
}

.secondary-btn {
  background-color: #eeeeee;
  color: #333;
}

.primary-btn:hover {
  background-color: #2a52b9;
}

.secondary-btn:hover {
  background-color: #d6d6d6;
}

.read-message {
  margin-top: 16px;
  color: green;
  font-weight: 500;
  font-size: 15px;
}
</style>