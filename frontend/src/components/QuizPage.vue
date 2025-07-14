<template>
  <div class="quiz-page-bg">
    <main class="main-content">
      <div class="profile-box">
        <div class="quiz-page" v-if="storyTitle && question.text">
          <h2>Quiz on "{{ storyTitle }}"</h2>
          <p><strong>Q:</strong> {{ question.text }}</p>
          <div class="options">
            <div v-for="(opt, index) in question.options" :key="index"
                 class="option-row"
                 :class="{
                   'wrong-answer': showFeedback && opt === question.selected && opt !== question.answer,
                   'correct-answer': locked && opt === question.answer
                 }">
              <label>
                <input type="radio" :value="opt" v-model="question.selected" :disabled="locked" />
                {{ opt }}
              </label>
            </div>
          </div>

          <div class="btn-group">
            <button @click="router.back()">Back</button>
            <button @click="submitAnswer" :disabled="!question.selected || locked">
              {{ locked ? 'Submitted' : 'Submit' }}
            </button>
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
const locked = ref(false)
const showFeedback = ref(false)

const question = ref({
  text: rawQuestion.value?.question || '',
  options: rawQuestion.value?.options || [],
  answer: rawQuestion.value?.answer || '',
  selected: ''
})

async function submitAnswer() {
  if (locked.value || !question.value.selected) return

  showFeedback.value = true

  if (question.value.selected === question.value.answer) {
    const token = localStorage.getItem('access_token')
    try {
      const response = await fetch('http://localhost:5000/submit_quiz', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          story_title: storyTitle.value,
          selected_option: question.value.selected
        })
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Submission failed')

      locked.value = true
      alert('🎉 Correct! Well done!')
    } catch (err) {
      console.error('Submission error:', err)
      alert('Failed to submit answer. Try again.')
    }
  } else {
    alert('Wrong answer! Try again.')
  }
}
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
  border: 2px solid #28a745;
}

.wrong-answer {
  background-color: #f8d7da;
  border: 2px solid #dc3545;
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
  font-size: 1rem;
  margin-top: 1rem;
  color: #333;
}
</style>
