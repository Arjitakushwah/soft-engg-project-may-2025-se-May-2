<template>
  <div class="wrapper">
      <div class="search-container">
        <input type="text" placeholder="Search your topic here" v-model="search_Text" />
        <button @click="performSearch">Search</button>
      </div>

      <div class="result-box" v-for="(content, topic) in search_Results" :key="topic">
        <a :href="`/result/${topic}`" @click.prevent="performSearch(topic)">{{ topic }}</a>
      </div>

      <div v-if="error_Message" class="error-message">
        {{ error_Message }}
      </div>
    </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const search_Text = ref('')
const error_Message = ref('')
const search_Results = ref({
  Maths: 'Mathematicians develop a new algorithm reducing matrix multiplication time, breaking a 50-year-old record.',
  Science: 'NASA confirms evidence of water vapor plumes on Europa, a key sign in the search for extraterrestrial life.',
  Animal: 'A new species of giant trapdoor spider discovered in Australia, highlighting biodiversity in remote habitats.'
})


const router = useRouter()

async function performSearch(topic = null) {
  const searchValue = topic || search_Text.value.trim()
  if (!searchValue) {
    error_Message.value = 'Please enter a topic to search.'
    return
  }

  router.push(`/result/${searchValue}`)

  try {
    const response = await fetch('http://localhost:5000/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: searchValue })
    })

    const data = await response.json()

    if (!response.ok) {
      error_Message.value = data.error || 'Search failed.'
    } else {
      // Redirect to /result/:topic and pass data
      router.push({ name: 'Result', params: { topic: searchValue } })
    }
  } catch (err) {
    error_Message.value = 'Server error while searching.'
  }
}
</script>

<style scoped>
.wrapper {
  max-width: 95%;
  margin: 15px 15px;
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
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 6px;
}

button:hover {
  background-color: #2a52b9;
}

.result-box {
  margin-bottom: 10px;
  background-color: #e1e9f3;
  padding: 12px;
  border-radius: 6px;
}

.result-box a {
  color: #1e3a8a;
  font-weight: bold;
}

.card {
  background-color: #e8e88c;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
}

.card h4 {
  margin-bottom: 10px;
  color: #333;
}

.card p {
  color: #555;
}

.error-message {
  color: red;
  margin-top: 15px;
  font-weight: bold;
}

.card .back-button {
  float: right;
  font-size: 12px;
  padding: 4px 10px;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
}



.back-button:hover {
  background-color: #2a52b9;
}
</style>
