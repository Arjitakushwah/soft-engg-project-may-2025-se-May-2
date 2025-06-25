<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="branding">
        <h2 class="greeting">Hi, <span class="username">{{ childName }}</span></h2>
        </div>
        <p class="greeting">QuizPage</p>
      
      <button @click="logout" class="logout-button">Logout</button>
    </header>

    <main class="main-content">
      <!-- Future content can be added here -->
       <div class="profile-box">
          <div class="profile-header">{{ childName }}'s Profile</div>
            <div class="quiz-page">
            <h2 v-if="storyTitle">Quiz on "{{ storyTitle }}"</h2>
            <p v-else>Please go to the story page and click on Quiz to start.</p>

            <div v-if="storyTitle" v-for="(q, index) in questions" :key="index" class="question-block">
            <p><strong>Q{{ index + 1 }}:</strong> {{ q.question }}</p>
            <div class="options">
                <div
                v-for="(opt, i) in q.options"
                :key="i"
                class="option-row"
                :class="{
                    'correct-answer': submitted && opt === q.answer,
                    'wrong-answer': submitted && q.selected === opt && q.selected !== q.answer
                }"
                >
                <label>
                    <input
                    type="radio"
                    :name="'q' + index"
                    :value="opt"
                    v-model="q.selected"
                    :disabled="submitted"
                    />
                    {{ opt }}
                </label>
                </div>
            </div>
            <div v-if="submitted && q.selected !== q.answer" class="explanation">
                Correct Answer: <strong>{{ q.answer }}</strong>
            </div>
            </div>

            <div v-if="storyTitle" class="btn-group">
            <button @click="router.back()">Back</button>
            <button @click="submitted = true">Submit</button>
            </div>
            </div>
        </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const route = useRoute()
const router = useRouter()
const submitted = ref(false)
const storyTitle = ref(route.query.story || '')
const childName = ref('Child')



// Example fixed question list (you can customize this)
const questions = ref([
  {
    question: 'What did the character discover?',
    options: ['A treasure', 'A magical book', 'A spaceship', 'A secret door'],
    answer: 'A magical book',
    selected: ''
  },
  {
    question: 'What kind of animals did they meet?',
    options: ['Robots', 'Talking animals', 'Aliens', 'Pirates'],
    answer: 'Talking animals',
    selected: ''
  },
  {
    question: 'What did the character learn?',
    options: ['Greed', 'Revenge', 'Compassion', 'Silence'],
    answer: 'Compassion',
    selected: ''
  },
  {
    question: 'How did the journey end?',
    options: ['They were trapped forever', 'They returned wiser', 'They lost the book', 'They forgot everything'],
    answer: 'They returned wiser',
    selected: ''
  },
  {
    question: 'What was the main theme?',
    options: ['Magic and mischief', 'Honesty and courage', 'Adventure and learning', 'Fear and darkness'],
    answer: 'Adventure and learning',
    selected: ''
  }
])

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/child_story', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  const data = await res.json()
  if (res.ok) {
    childName.value = data.username || data.name
  }
})


const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', sans-serif;
  background-color: #f6f9fc;
  min-height: 100vh;
  color: #333;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background-color: #1e1e2f;
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.branding {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.greeting {
  font-size: 1.6rem;
  margin: 0;
}

.username {
  color: #00f7ff;
}

.subtitle {
  font-size: 1rem;
  color: #cbd5e1;
}

.logout-button {
  background-color: #ff4757;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.logout-button:hover {
  background-color: #e63946;
}

.main-content {
  padding: 2rem;
}

.profile-box {
  width: 100%;
  max-width: 600px;
}

.profile-header {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.input-as-button {
  padding: 8px 16px;
  background-color: #cce0ff;
  border: 1px solid #000;
  font-weight: bold;
  cursor: text;
  width: 240px;
  text-align: center;
}
.story-card {
  background-color: #e0e0e0;
  border: 1px solid #aaa;
  padding: 1rem;
  max-width: 400px;
  margin-top: 1rem;
}
.quiz-btn {
  margin-top: 1rem;
  padding: 8px 16px;
  background-color: #cce0ff;
  border: 1px solid #000;
  cursor: pointer;
  font-weight: bold;
}

.option-row {
  margin: 8px 0;
  padding: 6px 10px;
  border-radius: 6px;
}

.correct-answer {
  background-color: #d4edda; /* light green */
  border: 1px solid #28a745;
}

.wrong-answer {
  background-color: #f8d7da; /* light red */
  border: 1px solid #dc3545;
}

.explanation {
  font-size: 0.95rem;
  color: #333;
  margin-bottom: 1rem;
}


</style>