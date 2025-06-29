<template>
  <div class="quiz-page-bg">
    <main class="main-content">
      <div class="profile-box">
        <div class="quiz-page" v-if="storyTitle && question.text">
          <h2>Quiz on "{{ storyTitle }}"</h2>
          <p><strong>Q:</strong> {{ question.text }}</p>
          <div class="options">
            <div v-for="(opt, index) in question.options" :key="index" class="option-row" :class="{
          'correct-answer': submitted && opt === question.answer,
          'wrong-answer': submitted && question.selected === opt && question.selected !== question.answer
        }">
              <label>
                <input type="radio" :value="opt" v-model="question.selected" :disabled="submitted" />
                {{ opt }}
              </label>
            </div>
          </div>
          <div v-if="submitted && question.selected !== question.answer" class="explanation">
            Correct Answer: <strong>{{ question.answer }}</strong>
          </div>
          <div class="btn-group">
            <button @click="router.back()">Back</button>
            <button @click="submitted = true" :disabled="!question.selected">Submit</button>
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
const storyTitle = ref(route.query.story || '')
const rawQuestion = ref(route.query.question ? JSON.parse(route.query.question) : null)
const submitted = ref(false)
const childName = ref('Child')

const question = ref({
  text: rawQuestion.value?.text || '',
  options: rawQuestion.value?.options || [],
  answer: rawQuestion.value?.answer || '',
  selected: ''
})

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  const data = await res.json()
  if (res.ok) {
    childName.value = data.username || data.name
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.quiz-page-bg {
  font-family: 'Comic Neue', cursive;
  background: linear-gradient(to bottom right, #fffafc, #f0f8ff);
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  max-width: 700px;
}

.profile-box {
  background-color: #fff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.profile-header {
  font-size: 1.6rem;
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  text-align: center;
  margin-bottom: 1.5rem;
}

.quiz-page {
  background: #fff7f9;
  border-left: 5px solid #ff6a88;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1rem;
}

h2 {
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  margin-bottom: 1rem;
}

.options {
  margin: 1rem 0;
}

.option-row {
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 8px;
  background: #f0f8ff;
  font-family: 'Comic Neue', cursive;
}

.correct-answer {
  background-color: #d4edda;
  border: 1px solid #28a745;
}

.wrong-answer {
  background-color: #f8d7da;
  border: 1px solid #dc3545;
}

.btn-group {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-group button {
  background-color: #ff6a88;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 8px 16px;
  font-family: 'Fredoka One', cursive;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-group button:hover {
  background-color: #ff4870;
}

.explanation {
  font-size: 0.95rem;
  color: #333;
  margin-top: 1rem;
}
</style>