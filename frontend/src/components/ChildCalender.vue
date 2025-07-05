<template>
  <div class="child-calendar-bg">
    <main class="main-content">
      <div class="calendar-container">
        <h2>{{ childName }}'s Calendar</h2>
        <FullCalendar :options="calendarOptions" />
        <transition name="fade">
          <div v-if="selectedTasks.length" class="task-box">
            <div class="task-header">
              <h3>Tasks for {{ selectedDate }}</h3>
              <span class="close-btn" @click="closeTasks">✖</span>
            </div>
            <ul>
              <li v-for="(task, index) in selectedTasks" :key="index">
                <span v-if="selectedDate < today">{{ task.status === 'completed' ? '✅' : '❌' }}</span>
                <span v-else-if="selectedDate === today">🟡</span>
                {{ task.title }}
              </li>
            </ul>
          </div>
        </transition>
      </div>
    </main>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

const router = useRouter()
const childName = ref('Child')
const selectedDate = ref('')
const selectedTasks = ref([])
const today = new Date().toISOString().split('T')[0]
const rawEvents = [
  { title: 'Math Quiz', date: '2025-06-20', status: 'completed' },
  { title: 'Science Homework', date: '2025-06-20', status: 'pending' },
  { title: 'Reading Task', date: '2025-06-20', status: 'not_completed' },
  { title: 'Drawing', date: '2025-06-26', status: 'pending' }
]

const groupedDates = [...new Set(rawEvents.map(e => e.date))]
const simplifiedEvents = groupedDates.map(date => ({
  title: 'Tasks',
  date,
  status: 'grouped'
}))

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  initialDate: '2025-06-01',
  contentHeight: 300,
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  },
  events: simplifiedEvents,
  eventContent(arg) {
    return {
      html: `<div style="color: black; font-weight: bold;">${arg.event.title}</div>`
    }
  },
  eventClick(info) {
    const date = info.event.startStr
    selectedDate.value = date
    selectedTasks.value = rawEvents.filter(e => e.date === date)
  }
})

function closeTasks() {
  selectedTasks.value = []
  selectedDate.value = ''
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('', {
    headers: {
      Authorization: `Bearer ${token}`
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

.child-calendar-bg {
  font-family: 'Comic Neue', cursive;
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
}

.main-content {
  width: 100%;
  max-width: 700px;
  display: flex;
  justify-content: center;
}

.calendar-container {
  background: #fff;
  padding: 2rem;
  width: 100%;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.calendar-container h2 {
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  text-align: center;
  margin-bottom: 1.5rem;
}

.fc {
  font-size: 14px;
}

.fc .fc-toolbar-title {
  font-size: 1.2rem;
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
}

.fc-daygrid-day-number {
  font-size: 0.9rem;
}

.fc-event-title {
  font-size: 0.8rem;
}

.fc-daygrid-event {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.task-box {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 280px;
  background: #fff8f9;
  border: 1px solid #ff6a88;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  z-index: 999;
  font-size: 15px;
  animation: fadeIn 0.3s ease-in-out;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-header h3 {
  font-size: 1.1rem;
  color: #ff6a88;
  font-family: 'Fredoka One', cursive;
  margin: 0;
}

.close-btn {
  font-size: 1.2rem;
  cursor: pointer;
  color: #ff6a88;
}

.task-box ul {
  list-style-type: none;
  padding-left: 0;
  margin-top: 0.8rem;
}

.task-box li {
  margin: 0.5rem 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -55%);
  }

  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}
</style>