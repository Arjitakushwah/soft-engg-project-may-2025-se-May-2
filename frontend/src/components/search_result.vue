<template>
  <div class="card">
    <h4>{{ topic }}</h4>

    <p v-if="info">{{ info }}</p>
    <p v-else>No data found for "{{ topic }}"</p>
    
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const topic = route.params.topic

const search_Results = {
  Maths: 'Mathematicians develop a new algorithm reducing matrix multiplication time, breaking a 50-year-old record.',
  Science: 'NASA confirms evidence of water vapor plumes on Europa, a key sign in the search for extraterrestrial life.',
  Animal: 'A new species of giant trapdoor spider discovered in Australia, highlighting biodiversity in remote habitats.'
}

const info = ref('')
if (topic in search_Results) {
  info.value = search_Results[topic]
} else {
  info.value = ''
}


// onMounted(async () => {
//   const res = await fetch('post_req', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ topic })
//   })
//   const data = await res.json()
//   info.value = data.description || 'No details found.'
// })

</script>

<style scoped>
    .card {
      max-width: 90%;
      margin: 40px auto;
      padding: 24px;
      background: #f9f9b8;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .card h4 {
      margin-bottom: 10px;
      color: #333;
    }
    .card p {
      font-size: 16px;
      color: #444;
    }
    .button-container {
      display: flex;
      justify-content: flex-end;
      margin-top: 10px;
    }
    button {
      padding: 10px 20px;
      background-color: #1e3a8a;
      color: white;
      border: none;
      border-radius: 6px;
    }
</style>


