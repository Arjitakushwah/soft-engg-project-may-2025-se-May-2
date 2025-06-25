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
        <h3>{{ todayDate }}</h3>
            <input
                v-model="newTask"
                placeholder="Add new Task"
                class="task-button-input"
                @keyup.enter="addTask"
            />
      </div>

      <p><strong>Tasks for today</strong></p>

      <div v-for="(task, index) in tasks" :key="index" class="task-row">
        <span>{{ task.name }}</span>
        <button
          :class="task.completed ? 'completed' : 'pending'"
          @click="toggleTask(index)"
        >
          {{ task.completed ? 'Completed' : 'Pending' }}
        </button>
        <button class="delete-btn" @click="deleteTask(index)">Delete</button>
      </div>
    </div>
  </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const childName = ref('Child')
const router = useRouter()
const today = new Date()
const options = { day: 'numeric', month: 'long', year: 'numeric' }
const todayDate = today.toLocaleDateString('en-GB', options)
const newTask = ref('')
const tasks = ref([
  { name: 'School', completed: true },
  { name: 'Lunch', completed: true },
  { name: 'Homework', completed: false },
  { name: 'Tuition', completed: false },
  { name: 'Football', completed: false }
])

function addTask() {
  if (newTask.value.trim()) {
    tasks.value.push({ name: newTask.value.trim(), completed: false })
    newTask.value = ''
  }
}

function toggleTask(index) {
  tasks.value[index].completed = !tasks.value[index].completed
}

function deleteTask(index) {
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
  padding: 6px 12px;
  font-weight: bold;
  font-family: inherit;
  font-size: 14px;
  width: 160px;
  text-align: center;
  cursor: text;
}

.task-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.5rem 0;
  font-size: 1rem;
}

.pending {
  background-color: red;
  color: white;
  border: none;
  padding: 4px 12px;
  cursor: pointer;
  font-weight: bold;
}

.completed {
  background-color: green;
  color: white;
  border: none;
  padding: 4px 12px;
  cursor: pointer;
  font-weight: bold;
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


</style>
