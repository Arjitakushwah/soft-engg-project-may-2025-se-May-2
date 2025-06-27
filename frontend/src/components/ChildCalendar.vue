<template>
  <div class="dashboard-container">
    <main class="main-content">
      <!-- Future content can be added here -->
       <div class="calendar-container">
        <h2>Calendar Report</h2>
        <FullCalendar
            :options="calendarOptions"
            />
          <div v-if="selectedTasks.length" class="task-box">
            <h3>Tasks for {{ selectedDate }}</h3>
            <ul>
              <li v-for="(task, index) in selectedTasks" :key="index">
                <span v-if="selectedDate < today">{{ task.status === 'completed' ? '✅' : '❌' }}</span>
                <span v-else-if="selectedDate === today">🟡</span>
                {{ task.title }}
              </li>
            </ul>
          </div>
        </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

// Static sample data
const rawEvents = [
  { title: 'Math Quiz', date: '2025-06-20', status: 'completed' },
  { title: 'Science Homework', date: '2025-06-20', status: 'pending' },
  { title: 'Reading Task', date: '2025-06-20', status: 'not_completed' },
  { title: 'Drawing', date: '2025-06-26', status: 'pending' },
]

const childName = ref('Child')
const router = useRouter()
const selectedDate = ref('')
const selectedTasks = ref([])
const today = new Date().toISOString().split('T')[0]
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
  eventContent: function(arg) {
    return {
      html: `<div style="color: black; font-weight: bold;">${arg.event.title}</div>`
    }
  },
  eventClick: function(info) {
  const date = info.event.startStr

  if (selectedDate.value === date && selectedTasks.value.length > 0) {
    selectedTasks.value = []
    selectedDate.value = ''
  } else {
    selectedDate.value = date
    selectedTasks.value = rawEvents.filter(e => e.date === date)
  }
}

})

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/child_calendar', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const data = await res.json()
  if (res.ok) {
    childName.value = data.username || data.name
    // If dynamic events:
    // rawEvents.value = data.events
  } else {
    childName.value = 'Child'
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
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  background-color: #f6f9fc;
  min-height: calc(100vh - 100px); /* Adjust based on header height */
}

.calendar-container {
  background: white;
  padding: 10px;
  max-width: 300px; 
  width: 100%; 
  color: black;
  margin: 0 auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  box-sizing: border-box;
}

.fc {
  font-size: 12px;
}

.fc .fc-toolbar-title {
  font-size: 1rem;
}

.fc-daygrid-day-number {
  font-size: 0.75rem;
}

.fc-event-title {
  font-size: 0.7rem;
}

.fc-daygrid-event {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.task-box {
  position: absolute;
  top: 180px; /* adjust as needed */
  left: 350px; /* adjust as needed */
  width: 250px;
  padding: 10px;
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: 14px;
}
.task-box h3 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.task-box ul {
  list-style-type: none;
  padding-left: 0;
}
.task-box li {
  margin: 0.5rem 0;
}


</style>