<template>
  <div class="dashboard-container">
    <main class="main-content">
      <!-- Future content can be added here -->
       <div class="profile-box">
          <div class="profile-header">{{ childName }}'s Profile</div>
            <div class="quiz-page" v-if="storyTitle && question.text">
            <h2>Quiz on "{{ storyTitle }}"</h2>
            <p><strong>Q:</strong> {{ question.text }}</p>

            <div class="options">
              <div
                v-for="(opt, index) in question.options"
                :key="index"
                class="option-row"
                :class="{
                  'correct-answer': submitted && opt === question.answer,
                  'wrong-answer': submitted && question.selected === opt && question.selected !== question.answer
                }"
              >
                <label>
                  <input
                    type="radio"
                    :value="opt"
                    v-model="question.selected"
                    :disabled="submitted"
                  />
                  {{ opt }}
                </label>
              </div>
            </div>

            <div v-if="submitted && question.selected !== question.answer" class="explanation">
              Correct Answer: <strong>{{ question.answer }}</strong>
            </div>

            <div v-if="storyTitle" class="btn-group">
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
const questionText = ref(route.query.question || '')
const storyTitle = ref(route.query.story || '')
const rawQuestion = ref(route.query.question ? JSON.parse(route.query.question) : null)
const submitted = ref(false)
const childName = ref('Child')

// prepare one question
const question = ref({
  text: rawQuestion.value?.text || '',
  options: rawQuestion.value?.options || [],
  answer: rawQuestion.value?.answer || '',
  selected: ''
})


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
  max-width: 400px;
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