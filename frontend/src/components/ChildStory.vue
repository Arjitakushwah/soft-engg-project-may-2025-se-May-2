<template>
  <div class="dashboard-container">
    <div class="dashboard-wrapper">
      <main class="main-content">
        <div class="profile-header">{{ childName }}'s Story Corner</div>

        <div class="input-section">
          <input
            v-model="storyPrompt"
            placeholder="Enter a story topic (e.g. honesty, marble)"
            class="story-input"
            @keyup.enter="generateStory"
          />
          <button class="generate-btn" @click="generateStory" :disabled="loading">
            {{ loading ? 'Generating...' : 'Generate' }}
          </button>
        </div>

        <transition name="fade">
          <div v-if="displayTitle" class="story-card">
            <h3 class="story-title">{{ displayTitle }}</h3>
            <p class="story-content">{{ storyContent }}</p>
            <button class="quiz-btn" @click="goToQuiz">Take Quiz</button>
          </div>
        </transition>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const childName = ref('Child')
const displayTitle = ref('')
const storyContent = ref('')
const selectedQuestion = ref('')
const storyPrompt = ref('')
const loading = ref(false)

async function generateStory() {
  const input = storyPrompt.value.trim()
  if (!input) {
    alert('Please enter a story prompt')
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('You are not logged in')
    return
  }

  loading.value = true

  try {
    const response = await fetch('http://localhost:5000/generate_story', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ child_prompt: input })
    })

    const data = await response.json()

    if (!response.ok) {
      console.error('Server error:', data)
      alert(data.error || 'Failed to generate story.')
      loading.value = false
      return
    }

    displayTitle.value = data.story.title
    storyContent.value = data.story.content
    selectedQuestion.value = JSON.stringify(data.story.quiz)
  } catch (err) {
    console.error('Network error:', err)
    alert('Network error. Please try again.')
  } finally {
    loading.value = false
  }
}

function goToQuiz() {
  router.push({
    name: 'QuizPage',
    query: {
      story: displayTitle.value,
      question: selectedQuestion.value
    }
  })
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch('http://localhost:5000/child/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    if (res.ok) {
      childName.value = data.username || data.name || 'Child'
    }
  } catch (err) {
    console.error('User info fetch failed:', err)
  }
})
</script>

<style scoped>
/* Styling same as before */
.dashboard-container {
  font-family: 'Comic Neue', cursive;
  background: linear-gradient(135deg, #fff4f7, #f0f8ff);
  display: flex;
  justify-content: center;
  padding: 3rem 1rem;
  box-sizing: border-box;
}

.dashboard-wrapper {
  width: 100%;
  max-width: 700px;
}

.main-content {
  width: 100%;
}

.profile-header {
  font-size: 1.8rem;
  color: #ff6a88;
  font-family: 'Fredoka One', cursive;
  text-align: center;
  margin-bottom: 2rem;
}

.input-section {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.story-input {
  padding: 10px 16px;
  border-radius: 10px;
  border: 1px solid #aaa;
  font-size: 1rem;
  width: 60%;
  max-width: 300px;
}

.generate-btn {
  padding: 10px 16px;
  border-radius: 10px;
  background-color: #ff6a88;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s ease;
}

.generate-btn:disabled {
  background-color: #ffb6c1;
  cursor: not-allowed;
}

.generate-btn:hover:not(:disabled) {
  background-color: #e75470;
}

.story-card {
  background-color: #fff7f9;
  border-left: 5px solid #ff6a88;
  padding: 1.5rem;
  border-radius: 12px;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.story-title {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 0.5rem;
  font-family: 'Fredoka One', cursive;
}

.story-content {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

.quiz-btn {
  margin-top: 1rem;
  padding: 10px 16px;
  background-color: #cce0ff;
  border: 1px solid #000;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.quiz-btn:hover {
  background-color: #a8d0ff;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
