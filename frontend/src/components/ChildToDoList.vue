<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="branding">
        <h2 class="greeting">Hi, <span class="username">{{ childName }}</span></h2>
        </div>
        <p class="greeting">To-Do-Lisit</p>
      
      <button @click="logout" class="logout-button">Logout</button>
    </header>

    <main class="main-content">
    <div class="task-box">
      <div class="task-header">
      <div class="date-nav">
        <button @click="goToPreviousDay" class="nav-arrow">&lt;</button>
        <span class="date-text">{{ todayDate }}</span>
        <button @click="goToNextDay" class="nav-arrow">&gt;</button>
      </div>

      <input
        v-model="newTask"
        placeholder="Add new Task"
        class="task-button-input"
        @keyup.enter="addTask"
        :disabled="!isCurrentDateToday"
      />
    </div>


      <p><strong>Tasks for today</strong></p>

      <div v-for="(task, index) in tasks" :key="index" class="task-row">
        <span>{{ task.name }}</span>
        <button
          :class="task.completed ? 'completed' : 'pending'"
          @click="isCurrentDateToday && toggleTask(index)"
          :disabled="!isCurrentDateToday"
        >
          {{ task.completed ? 'Completed' : 'Pending' }}
        </button>

        <button
          class="delete-btn"
          @click="isCurrentDateToday && deleteTask(index)"
          :disabled="!isCurrentDateToday"
        >
          Delete
        </button>

      </div>
    </div>
  </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Format helper
function formatDate(date) {
  return date.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}
function getDateKey(date) {
  return date.toISOString().split('T')[0]
}

const childName = ref('Child')
const router = useRouter()

const currentDate = ref(new Date())
const todayDate = ref(formatDate(currentDate.value))
const isCurrentDateToday = ref(isToday(currentDate.value))


const newTask = ref('')

// Default template tasks
const defaultTasks = [
  { name: 'School', completed: false },
  { name: 'Lunch', completed: false },
  { name: 'Homework', completed: false },
  { name: 'Tuition', completed: false },
  { name: 'Football', completed: false }
]

// Object to store tasks by date
const tasksByDate = ref({
  [getDateKey(currentDate.value)]: defaultTasks.map(task => ({ ...task }))  // clone
})

const tasks = ref([])

function loadTasksForDate(date) {
  const key = getDateKey(date)
  if (!tasksByDate.value[key]) {
    // If no task exists for the date, initialize with default tasks
    tasksByDate.value[key] = defaultTasks.map(task => ({ ...task }))
  }
  tasks.value = tasksByDate.value[key]
  todayDate.value = formatDate(date)
  isCurrentDateToday.value = isToday(date)
}

function isToday(date) {
  const today = new Date()
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  )
}

function goToPreviousDay() {
  currentDate.value.setDate(currentDate.value.getDate() - 1)
  loadTasksForDate(currentDate.value)
}

function goToNextDay() {
  currentDate.value.setDate(currentDate.value.getDate() + 1)
  loadTasksForDate(currentDate.value)
}

function addTask() {
  const key = getDateKey(currentDate.value)
  if (!tasksByDate.value[key]) {
    tasksByDate.value[key] = []
  }

  if (newTask.value.trim()) {
    const taskObj = { name: newTask.value.trim(), completed: false }
    tasksByDate.value[key].push(taskObj)
    tasks.value = tasksByDate.value[key]  // refresh tasks list
    newTask.value = ''
  }
}

function toggleTask(index) {
  tasks.value[index].completed = !tasks.value[index].completed
}

function deleteTask(index) {
  const key = getDateKey(currentDate.value)
  tasksByDate.value[key].splice(index, 1)
  tasks.value.splice(index, 1)
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/child_todolist', {
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

  // Initial task load
  loadTasksForDate(currentDate.value)
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
  background-color: white;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: start;
  padding: 2rem;
}

.task-box {
  background-color: white; 
  padding: 1.5rem;
  width: 100%;
  max-width: 500px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.task-button-input {
  border: 1px solid #000;
  background-color: #cce0ff;
  padding: 4px 10px;               /* Smaller padding */
  font-weight: bold;
  font-family: inherit;
  font-size: 13px;                 /* Slightly smaller text */
  width: 120px;                    /* Slightly smaller width */
  border-radius: 8px;              /* Rounded corners */
  text-align: center;
  cursor: text;
}

.task-row {
  display: grid;
  grid-template-columns: 1fr 120px 80px; /* 3 columns: name, status, delete */
  align-items: center;
  gap: 10px;
  margin: 0.5rem 0;
}

.pending,
.completed {
  width: 100px;            /* consistent width */
  text-align: center;      /* center the text */
  padding: 6px 0;          /* equal vertical padding */
  font-size: 14px;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.pending {
  background-color: red;
  color: white;
}

.completed {
  background-color: green;
  color: white;
}


.task-actions {
  display: flex;
  gap: 0.5rem;
}

.delete-btn {
  background-color: #888;
  color: white;
  border: none;
  padding: 4px 10px;
  cursor: pointer;
  font-weight: bold;
  border-radius: 4px;
}

.delete-btn:hover {
  background-color: #555;
}

.back-arrow {
  background: none;
  border: none;
  font-size: 1.5rem;
  margin-right: 10px;
  cursor: pointer;
  color: #333;
  font-weight: bold;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.nav-arrow {
  background: none;
  border: 1px solid #333;
  font-size: 0.9rem;       /* smaller text */
  padding: 2px 6px;        /* smaller button box */
  margin: 0 6px;
  border-radius: 4px;      /* slightly rounded */
  cursor: pointer;
  color: #333;
  background-color: #f0f0f0;
}


</style>
