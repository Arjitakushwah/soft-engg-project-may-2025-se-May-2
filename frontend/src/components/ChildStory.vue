<template>
  <div class="dashboard-container">
    <div class="dashboard-wrapper">
      <main class="main-content">

        <div v-if="viewMode === 'story'">
          <div class="profile-header">{{ childName }}'s Story Corner</div>

          <div v-if="message" :class="['message', messageType === 'error' ? 'message-error' : 'message-success']">
            {{ message }}
          </div>

          <div class="dual-action-bar">
            <div class="action-group create-group">
              <input
                v-model="storyPrompt"
                placeholder="Enter a topic to create a story..."
                class="action-input"
                @keyup.enter="generateStory"
              />
              <button class="generate-btn" @click="generateStory" :disabled="loading">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.71 0L11 10l-1.5 1.5 3.54 3.54 5.5-5.5h3.11v-2H22l-1.64-1.64z"/><path d="m14.83 7.17 5.5 5.5"/><path d="M12 15h.01"/></svg>
                <span>Create</span>
              </button>
            </div>
            
            <div class="separator"></div>

            <div class="action-group search-group">
              <input
                v-model="searchQuery"
                placeholder="Search your past stories..."
                class="action-input"
                @keyup.enter="searchStories"
              />
              <select v-model="searchBy" class="search-select">
                <option value="theme">by Theme</option>
                <option value="title">by Title</option>
                <option value="date">by Date</option>
              </select>
              <button class="search-btn" @click="searchStories" :disabled="loading">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <span>Search</span>
              </button>
            </div>
          </div>

          <transition name="fade" mode="out-in">
            <div v-if="showStoryList" class="story-list-container">
              <h3 class="story-list-header">Search Results</h3>
              <ul v-if="stories.length > 0" class="story-list">
                <li v-for="story in stories" :key="story.id" @click="displayStory(story, true)" class="story-list-item">
                  <span class="story-list-title">{{ story.title }}</span>
                  <span class="story-list-date">{{ formatDate(story.created_at) }}</span>
                </li>
              </ul>
              <div v-else class="empty-results">
                No stories found matching your search
              </div>
            </div>
            <div v-else-if="displayTitle" class="story-card">
              <h3 class="story-title">{{ displayTitle }}</h3>
              <p class="story-content">{{ storyContent }}</p>
              <button v-if="!isFromHistory && !isQuizCompleted" class="quiz-btn" @click="goToQuiz">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>Take Quiz</span>
              </button>
            </div>
            <div v-else class="prompt-container">
               <svg class="action-svg rocket" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.3.7-3.29s-.01-2.45-.7-3.29c-1.26-1.5-5-2-5-2s.74 3.5 2 5z"/><path d="m12 15-3-3a9 9 0 0 1 3-7 9 9 0 0 1 7 3 9 9 0 0 1-7 7z"/></svg>
              <h3>Let's Start a New Adventure!</h3>
              <p>Create a new story or search your past adventures</p>
            </div>
          </transition>
        </div>

        <div v-if="viewMode === 'quiz'" class="story-card quiz-mode">
          <div class="quiz-header">
            <h2>Quiz: {{ displayTitle }}</h2>
            <p class="quiz-subheader">Test what you learned from the story</p>
          </div>
          
          <div v-if="!quizSubmitted" class="quiz-content">
            <h3 class="quiz-question">{{ quizQuestion }}</h3>
            <div class="options-grid">
              <button v-for="(option, index) in quizOptions" :key="index" class="option-btn" @click="submitAnswer(option)" :disabled="loading">
                <span class="option-letter">{{ String.fromCharCode(65 + index) }}</span>
                <span class="option-text">{{ option }}</span>
              </button>
            </div>
          </div>
          
          <div v-else class="result-view">
            <div v-if="isCorrect" class="result-content">
               <div class="svg-container">
                  <svg class="result-svg checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>
               </div>
              <h2 class="result-text correct-text">Correct!</h2>
              <p class="result-feedback">Great job! You understood the story well.</p>
            </div>
            <div v-else class="result-content">
               <div class="svg-container">
                  <svg class="result-svg cross" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="cross-circle" cx="26" cy="26" r="25" fill="none"/><path class="cross-path" fill="none" d="M16 16 36 36 M36 16 16 36"/></svg>
               </div>
              <h2 class="result-text wrong-text">Not Quite</h2>
              <p class="result-feedback">Review the story and try again!</p>
            </div>
            <button @click="returnToStoryView" class="back-btn">
                {{ isCorrect ? 'Finish' : 'Try Again' }}
            </button>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const childName = ref('Child');
const displayTitle = ref('');
const storyContent = ref('');
const selectedQuestion = ref('');
const loading = ref(false);
const message = ref('');
const messageType = ref('');
const stories = ref([]);
const showStoryList = ref(false);
const isFromHistory = ref(false);
const viewMode = ref('story');
const quizQuestion = ref('');
const quizOptions = ref([]);
const quizSubmitted = ref(false);
const isCorrect = ref(false);
const isQuizCompleted = ref(false);
const storyPrompt = ref('');
const searchQuery = ref('');
const searchBy = ref('theme');

function formatDate(dateString) {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

function showMessage(text, type, duration = 4000) {
  message.value = text;
  messageType.value = type;
  setTimeout(() => { message.value = ''; }, duration);
}

function displayStory(story, isHistoric = false) {
  displayTitle.value = story.title;
  storyContent.value = story.content;
  selectedQuestion.value = JSON.stringify(story.quiz);
  isFromHistory.value = isHistoric;
  showStoryList.value = false;
  isQuizCompleted.value = story.quizCompleted || false;
  if (!isHistoric) {
    sessionStorage.setItem('lastStory', JSON.stringify(story));
  }
}

async function searchStories() {
  const query = searchQuery.value.trim();
  if (!query) {
    return showMessage('Please enter something to search for.', 'error');
  }
  loading.value = true;
  displayTitle.value = '';
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('You must be logged in to search stories.');
    const response = await fetch(`http://localhost:5000/stories?by=${searchBy.value}&query=${query}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to fetch stories.');
    stories.value = data.stories;
    showStoryList.value = true;
    if (stories.value.length === 0) {
      showMessage('No stories found matching your search.', 'success');
    }
  } catch (err) {
    showMessage(err.message, 'error');
    stories.value = [];
  } finally {
    loading.value = false;
  }
}

async function generateStory() {
  const prompt = storyPrompt.value.trim();
  if (!prompt) {
    return showMessage('Please enter a story prompt', 'error');
  }
  loading.value = true;
  showStoryList.value = false;
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('You are not logged in.');
    const response = await fetch('http://localhost:5000/generate_story', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ child_prompt: prompt }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to generate story.');
    
    const newStory = {
      title: data.story.title,
      content: data.story.content,
      quiz: data.story.quiz,
      quizCompleted: false,
      created_at: new Date().toISOString()
    };
    displayStory(newStory, false);
    showMessage('Story generated successfully!', 'success');
  } catch (err) {
    showMessage(err.message, 'error');
  } finally {
    loading.value = false;
  }
}

function goToQuiz() {
  try {
    const quizData = JSON.parse(selectedQuestion.value);
    quizQuestion.value = quizData.question;
    quizOptions.value = quizData.options;
    quizSubmitted.value = false;
    isCorrect.value = false;
    viewMode.value = 'quiz';
  } catch (e) {
    showMessage('Could not start the quiz.', 'error');
  }
}

async function submitAnswer(selectedOption) {
  loading.value = true;
  await new Promise(resolve => setTimeout(resolve, 300)); // For UX effect
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('Authentication token not found.');

    const response = await fetch('http://localhost:5000/submit_quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        story_title: displayTitle.value,
        selected_option: selectedOption
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to submit the answer.');
    }

    // THE KEY FIX: Directly use the boolean value from the backend
    isCorrect.value = data.is_correct;
    
    // Show the result screen (correct/incorrect)
    quizSubmitted.value = true; 

  } catch (error) {
    showMessage(error.message, 'error');
    quizSubmitted.value = false; // Don't get stuck on the result screen if API fails
  } finally {
    loading.value = false;
  }
}

function returnToStoryView() {
  // If the answer was correct, the quiz is over.
  if (isCorrect.value) {
    showMessage('Correct! Great job! 🎉', 'success');
    isQuizCompleted.value = true; 
    sessionStorage.removeItem('lastStory');
    
    // Reset state to show the initial "Create a new story" prompt
    displayTitle.value = '';
    storyContent.value = '';
    viewMode.value = 'story';
    quizSubmitted.value = false; // Reset for the next story's quiz
  } else {
    // If the answer was wrong, send the user back to the story to re-read.
    showMessage('That was not quite right. Read the story and give it another try!', 'error');
    viewMode.value = 'story';      // Return to the story view
    quizSubmitted.value = false; // Reset the quiz so they can try again from the start
  }
}

onMounted(async () => {
  const lastStoryRaw = sessionStorage.getItem('lastStory');
  if (lastStoryRaw) {
    try { displayStory(JSON.parse(lastStoryRaw), false); } 
    catch (e) { sessionStorage.removeItem('lastStory'); }
  }
  try {
    const token = localStorage.getItem('access_token');
    const res = await fetch('http://localhost:5000/child/me', { headers: { Authorization: `Bearer ${token}` } });
    const data = await res.json();
    if (res.ok) { childName.value = data.username || data.name || 'Child'; }
  } catch (err) { console.error('User info fetch failed:', err); }
});
</script>

<style scoped>
.dashboard-container {
  font-family: 'Comic Neue', cursive;
  background-color: #F0F8FF;
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  min-height: 100vh;
}
.dashboard-wrapper { 
  width: 100%; 
  max-width: 900px;
}
.main-content { width: 100%; }
.profile-header, .story-list-header, .story-title, .quiz-question, 
.result-text, .prompt-container h3, .action-header, .quiz-header h2 {
  font-family: 'Fredoka One', cursive;
}
.profile-header {
  font-size: 2.2rem;
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
}

.dual-action-bar {
  display: flex;
  gap: 1.5rem;
  background: #FFFFFF;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  margin-bottom: 2rem;
  align-items: center;
}
.action-group {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  width: 100%;
}
.create-group {
  flex: 1;
}
.search-group {
  flex: 1.5;
}
.action-input {
  flex-grow: 1;
  padding: 14px 18px;
  border-radius: 10px;
  border: 2px solid #E0E0E0;
  font-size: 1.05rem;
  transition: border-color 0.2s;
  min-width: 0; /* Allows input to shrink properly */
}
.action-input:focus {
  outline: none;
  border-color: #ff6a88;
}
.separator {
  width: 2px;
  height: 50px;
  background-color: #E0E0E0;
}
.search-select {
  padding: 14px 10px;
  border-radius: 10px;
  border: 2px solid #E0E0E0;
  background-color: white;
  font-size: 1.05rem;
  font-family: 'Comic Neue', cursive;
  min-width: 120px;
}
.search-select:focus { 
  outline: none; 
  border-color: #5c9ce5;
}

.generate-btn, .search-btn, .quiz-btn, .back-btn {
  padding: 14px 16px;
  border-radius: 10px;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1.05rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}
.generate-btn svg, .search-btn svg, .quiz-btn svg, .action-svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
  fill: none;
  stroke-width: 2.5;
}
.generate-btn { 
  background-color: #ff6a88; 
  min-width: 110px;
}
.search-btn { 
  background-color: #5c9ce5; 
  min-width: 110px;
}
.generate-btn:hover, .search-btn:hover, .quiz-btn:hover, .back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.story-card, .story-list-container, .prompt-container {
  background-color: #FFFFFF;
  border-radius: 16px;
  padding: 2rem;
  margin-top: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
}
.story-title { 
  font-size: 1.8rem; 
  color: #333; 
  margin-bottom: 1rem;
}
.story-content { 
  font-size: 1.1rem; 
  color: #555; 
  line-height: 1.8; 
  margin-bottom: 1.5rem;
}
.story-list-header { 
  text-align: center; 
  font-size: 1.5rem; 
  margin-bottom: 1.5rem;
}
.story-list { 
  list-style: none; 
  padding: 0; 
  margin: 0;
}
.story-list-item { 
  padding: 1rem; 
  border-radius: 8px; 
  margin-bottom: 0.5rem; 
  cursor: pointer; 
  transition: background-color 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.story-list-item:hover { 
  background-color: #F0F8FF; 
}
.story-list-title {
  font-weight: bold;
  font-size: 1.1rem;
}
.story-list-date {
  color: #888;
  font-size: 0.9rem;
}
.empty-results {
  text-align: center;
  color: #888;
  padding: 2rem;
  font-size: 1.1rem;
}

.prompt-container { 
  text-align: center; 
  border: 2px dashed #E0E0E0; 
  padding: 3rem 2rem;
}
.prompt-container h3 { 
  margin-top: 0; 
  color: #333; 
  font-size: 1.5rem;
}
.prompt-container p {
  color: #666;
  font-size: 1.1rem;
}
.prompt-container .rocket { 
  width: 60px; 
  height: 60px; 
  color: #ff6a88; 
  margin-bottom: 1.5rem; 
}
.message { 
  padding: 1rem; 
  border-radius: 8px; 
  margin-bottom: 1.5rem; 
  text-align: center; 
  font-weight: bold; 
  font-size: 1.1rem;
}
.message-success { 
  background-color: #E6F7E9; 
  color: #28a745; 
}
.message-error { 
  background-color: #FDE8E8; 
  color: #dc3545; 
}
.fade-enter-active, .fade-leave-active { 
  transition: opacity 0.3s ease; 
}
.fade-enter-from, .fade-leave-to { 
  opacity: 0; 
}

/* Quiz Styles */
.quiz-mode { 
  border: 3px solid #5c9ce5; 
  padding: 2.5rem;
}
.quiz-header {
  text-align: center;
  margin-bottom: 2rem;
}
.quiz-header h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 0.5rem;
}
.quiz-subheader {
  color: #666;
  font-size: 1.1rem;
}
.quiz-question { 
  text-align: center; 
  font-size: 1.5rem; 
  line-height: 1.4; 
  margin-bottom: 2rem;
  color: #444;
}
.options-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 1.2rem; 
  margin-bottom: 1.5rem;
}
.option-btn {
  padding: 1.2rem;
  font-size: 1.1rem;
  border-radius: 12px;
  border: 2px solid #E0E0E0;
  background-color: #FFFFFF;
  cursor: pointer;
  display: flex;
  align-items: center;
  text-align: left;
  transition: all 0.2s;
}
.option-btn:hover {
  border-color: #5c9ce5;
  background-color: #f5f9ff;
}
.option-letter {
  background-color: #5c9ce5;
  color: white;
  border-radius: 8px;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 1.2rem;
  font-family: 'Fredoka One', cursive;
  font-size: 1.1rem;
}
.result-view { 
  display: flex; 
  flex-direction: column; 
  align-items: center;
  text-align: center;
}
.svg-container { 
  margin-bottom: 1.5rem; 
}
.result-svg { 
  width: 120px; 
  height: 120px; 
}
.result-text { 
  font-size: 2.5rem; 
  margin: 0 0 0.5rem 0; 
}
.result-feedback {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  max-width: 80%;
}
.correct-text { 
  color: #28a745; 
}
.wrong-text { 
  color: #dc3545; 
}
.back-btn { 
  background-color: #ff6a88; 
  padding: 14px 24px; 
  border-radius: 10px; 
  border: none; 
  color: white; 
  font-weight: bold; 
  font-size: 1.1rem; 
  cursor: pointer; 
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 1rem;
}
.quiz-btn { 
  background-color: #28a745; 
  padding: 14px 24px; 
  border-radius: 10px; 
  border: none; 
  color: white; 
  font-weight: bold; 
  font-size: 1.1rem; 
  cursor: pointer; 
  transition: transform 0.2s, box-shadow 0.2s; 
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

/* Quiz SVG Animations */
.checkmark-circle { 
  stroke-dasharray: 157; 
  stroke-dashoffset: 157; 
  stroke-width: 3; 
  stroke: #28a745; 
  animation: draw 0.5s ease-out forwards; 
}
.checkmark-check { 
  stroke-dasharray: 48; 
  stroke-dashoffset: 48; 
  stroke-width: 4; 
  stroke: #28a745; 
  animation: draw 0.4s 0.3s ease-out forwards; 
}
.cross-circle { 
  stroke-dasharray: 157; 
  stroke-dashoffset: 157; 
  stroke-width: 3; 
  stroke: #dc3545; 
  animation: draw 0.5s ease-out forwards; 
}
.cross-path { 
  stroke-dasharray: 48; 
  stroke-dashoffset: 48; 
  stroke-width: 4; 
  stroke: #dc3545; 
  animation: draw 0.2s 0.5s ease-out forwards; 
}
@keyframes draw { 
  to { stroke-dashoffset: 0; } 
}

@media (max-width: 850px) {
  .dual-action-bar { 
    flex-direction: column; 
    gap: 1rem;
  }
  .separator { 
    display: none; 
  }
  .action-group { 
    width: 100%;
  }
  .options-grid { 
    grid-template-columns: 1fr; 
  }
  .profile-header { 
    font-size: 1.8rem; 
  }
  .action-input, .search-select {
    padding: 12px 14px;
  }
  .generate-btn, .search-btn {
    padding: 12px 14px;
  }
}

@media (max-width: 600px) {
  .dashboard-container {
    padding: 1rem 0.5rem;
  }
  .story-card, .story-list-container {
    padding: 1.5rem;
  }
  .story-title {
    font-size: 1.5rem;
  }
  .quiz-header h2 {
    font-size: 1.5rem;
  }
}
</style>