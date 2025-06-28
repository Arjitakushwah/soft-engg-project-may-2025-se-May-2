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
            <button class="generate-btn" @click="generateStory">Generate</button>
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
  const storyTitle = ref('')
  const displayTitle = ref('')
  const storyContent = ref('')
  const selectedQuestion = ref('')
  const storyPrompt = ref('')
  
  let currentIndex = 0
  
  const storyList = [
    {
      title: 'The Lost Marble',
      content: name => `One day, ${name} found a shiny red marble on the school playground. They knew it wasn’t theirs, but they liked it so much that they slipped it into their pocket. Later, their friend Ravi was sad—he had lost his favorite marble. ${name} felt a twist in the tummy. At home, they told their mom, who gently said, “Being honest is always the right choice.” The next day, ${name} returned the marble to Ravi and said sorry. Ravi smiled and forgave them. ${name} felt light and happy.`,
      question: {
        text: 'What lesson did the child learn from the marble incident?',
        options: ['Be sneaky', 'Be honest', 'Take things quietly', 'Keep secrets'],
        answer: 'Be honest'
      }
    },
    {
      title: 'The Broken Toy',
      content: name => `${name} borrowed a toy from their friend but accidentally broke it. They felt bad and didn’t know what to do. Finally, they told the truth to their friend and offered to fix it. Their friend appreciated the honesty.`,
      question: {
        text: 'How did the child handle breaking the toy?',
        options: ['Ignored it', 'Blamed someone else', 'Told the truth', 'Hid the toy'],
        answer: 'Told the truth'
      }
    }
  ]
  
  function generateStory() {
    const input = storyPrompt.value.toLowerCase().trim()
  
    const matchedStory = storyList.find(
      story =>
        (input.includes('marble') && story.title === 'The Lost Marble') ||
        (input.includes('honest') && story.title === 'The Lost Marble') ||
        (input.includes('toy') && story.title === 'The Broken Toy') ||
        (input.includes('truth') && story.title === 'The Broken Toy')
    )
  
    const story = matchedStory || storyList[currentIndex % storyList.length]
  
    displayTitle.value = story.title
    storyContent.value = story.content(childName.value)
    selectedQuestion.value = JSON.stringify(story.question)
    currentIndex++
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
      const token = localStorage.getItem('token')
      const res = await fetch('http://127.0.0.1:5000/child_story', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
  
      const data = await res.json()
  
      if (res.ok) {
        childName.value = data.username || data.name
      } else {
        console.warn('Invalid token or server error')
        childName.value = 'Child'
      }
    } catch (err) {
      console.error('API error:', err)
      childName.value = 'Child'
    }
  })
  </script>
  
  <style scoped>
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
  
  .generate-btn:hover {
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
  