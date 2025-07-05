<template>
  <div class="todo-page">
    <div class="top-controls">
      <div class="date-nav">
        <button @click="goToPreviousDay" class="nav-arrow">&lt;</button>
        <span class="date-text">{{ todayDate }}</span>
        <button @click="goToNextDay" class="nav-arrow">&gt;</button>
      </div>
      <input v-model="newTask" placeholder="Add new Task" class="task-input" @keyup.enter="addTask"
        :disabled="!isCurrentDateToday" />
    </div>
    <p class="task-title">Tasks</p>
    <div v-for="(task, index) in currentTasks" :key="index" class="task-row">
      <span class="task-name">{{ task.name }}</span>
      <div class="actions">
        <button v-if="!task.completed" class="btn complete" @click="markCompleted(index)"
          :disabled="!isCurrentDateToday">
          Completed
        </button>
        <button v-else class="btn pending" @click="markPending(index)" :disabled="!isCurrentDateToday">
          Pending
        </button>
        <button class="btn delete" @click="deleteTask(index)" :disabled="!isCurrentDateToday">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const getDateKey = (date) => date.toISOString().split('T')[0]
const formatDate = (date) =>
  date.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
const isToday = (date) => {
  const today = new Date()
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  )
}

const currentDate = ref(new Date())
const newTask = ref('')
const todayDate = ref(formatDate(currentDate.value))
const isCurrentDateToday = ref(isToday(currentDate.value))

const taskMap = reactive({
  [getDateKey(currentDate.value)]: [
    { name: 'Read story', completed: false },
    { name: 'Play outside', completed: true },
    { name: 'Water plants', completed: false }
  ],
  [getDateKey(new Date(new Date().setDate(new Date().getDate() - 1)))]: [
    { name: 'Clean your room', completed: true },
    { name: 'Draw a house', completed: false }
  ],
  [getDateKey(new Date(new Date().setDate(new Date().getDate() + 1)))]: [
    { name: 'Do Maths practice', completed: true },
    { name: 'Help mom', completed: true }
  ]
})

const currentTasks = computed(() => {
  const key = getDateKey(currentDate.value)
  if (!taskMap[key]) taskMap[key] = []
  return taskMap[key]
})

function loadTasksForDate(date) {
  todayDate.value = formatDate(date)
  isCurrentDateToday.value = isToday(date)
}
function addTask() {
  const key = getDateKey(currentDate.value)
  if (!taskMap[key]) taskMap[key] = []
  if (newTask.value.trim()) {
    taskMap[key].push({ name: newTask.value.trim(), completed: false })
    newTask.value = ''
  }
}
function markCompleted(index) {
  currentTasks.value[index].completed = true
}

function markPending(index) {
  currentTasks.value[index].completed = false
}

function deleteTask(index) {
  currentTasks.value.splice(index, 1)
}

function goToPreviousDay() {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() - 1)
  currentDate.value = newDate
  loadTasksForDate(newDate)
}

function goToNextDay() {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() + 1)
  currentDate.value = newDate
  loadTasksForDate(newDate)
}

loadTasksForDate(currentDate.value)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.todo-page {
  padding: 5rem;
  font-family: 'Comic Neue', cursive;
  /* background: linear-gradient(to bottom right, #f0f8ff, #ffe6f0); */
  min-height: 100%;
}

.top-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 3rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.date-nav {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.date-text {
  font-family: 'Fredoka One', cursive;
  font-size: 1.5rem;
  color: #ff6a88;
}

.nav-arrow {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #1e3a8a;
  cursor: pointer;
}

.task-input {
  flex: 1;
  min-width: 200px;
  padding: 10px;
  border: 1px solid #ff6a88;
  border-radius: 10px;
  background: #fff;
  font-family: 'Comic Neue', cursive;
}

.task-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: #333;
}

.task-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9e6e6;
  border-left: 5px solid #ff6a88;
  padding: 15px 20px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
}

.task-name {
  flex: 1;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 6px 10px;
  border-radius: 8px;
  font-family: 'Comic Neue', cursive;
  border: none;
  cursor: pointer;
}

.complete {
  background-color: #28a745;
  color: white;
}

.pending {
  background-color: #ffc107;
  color: black;
}

.delete {
  background-color: #fd466e;
  color: white;
}
</style>