<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="branding">
        <h2 class="greeting">Hi, <span class="username">{{ childName }}</span></h2>
        </div>
        <p class="greeting">StoryBoard</p>
      
      <button @click="logout" class="logout-button">Logout</button>
    </header>

    <main class="main-content">
      <!-- Future content can be added here -->
       <div class="profile-box">
          <div class="profile-header">{{ childName }}'s Profile</div>
          <div class="story-container">
                <div class="input-header">
                <input
                    v-model="storyTitle"
                    placeholder="Enter story title"
                    @keyup.enter="generateStory"
                    class="input-as-button"
                />
                </div>

                <div v-if="displayTitle" class="story-card">
                    <h3>{{ displayTitle }}</h3>
                    <p>{{ storyContent }}</p>
                    <button
                        class="quiz-btn"
                        @click="goToQuiz"
                        >
                        Quiz
                    </button>
                </div>
            </div>
        </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const childName = ref('Child')
const storyTitle = ref('')
const displayTitle = ref('')
const storyContent = ref('')


function generateStory() {
  if (storyTitle.value.trim()) {
    displayTitle.value = storyTitle.value.trim()
    storyContent.value = `One day, ${name} found a shiny red marble on the school playground. They knew it wasn’t theirs, but they liked it so much that they slipped it into their pocket. Later, their friend Ravi was sad—he had lost his favorite marble. ${name} felt a twist in the tummy. At home, they told their mom, who gently said, “Being honest is always the right choice.” The next day, ${name} returned the marble to Ravi and said sorry. Ravi smiled and forgave them. ${name} felt light and happy.`
    storyTitle.value = ''
  }
}

function goToQuiz() {
  router.push({ name: 'QuizPage', query: { story: displayTitle.value } })
}

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
  } else {
    childName.value = 'Child'
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

</style>