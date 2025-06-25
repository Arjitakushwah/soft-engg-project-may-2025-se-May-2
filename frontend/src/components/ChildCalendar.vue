<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="branding">
        <h2 class="greeting">Hi, <span class="username">{{ childName }}</span></h2>
        </div>
        <p class="greeting">Calendar Report</p>
      
      <button @click="logout" class="logout-button">Logout</button>
    </header>

    <main class="main-content">
      <!-- Future content can be added here -->
       <div class="calendar-container">
        <h2>Calendar Report</h2>
        <FullCalendar
            :options="calendarOptions"
            />
        </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

const childName = ref('Child')
const router = useRouter()
const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  initialDate: '2025-06-01',
  contentHeight: 400,
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  },
  events: [
    { title: 'Event 1', date: '2025-06-20' },
    { title: 'Event 2', date: '2025-06-25' }
  ]
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
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  background-color: #f6f9fc;
  min-height: calc(100vh - 100px); /* Adjust based on header height */
}

.calendar-container {
  background: white;
  padding: 16px;
  max-width: 800px; 
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

</style>