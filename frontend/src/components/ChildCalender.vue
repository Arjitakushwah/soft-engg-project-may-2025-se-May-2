<template>
  <div class="child-calendar-bg">
    <main class="main-content">
      <div class="calendar-container">
        <div class="calendar-title">
          <svg class="cal-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
              <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/> 
          </svg>
          <h1 style="margin-top: 19px;">{{ childName }}'s Calendar</h1>
        </div>
        <FullCalendar v-if="calendarOptions" :options="calendarOptions" />
        <div class="legend">
          <span class="label">Minimal Done</span>
          <span class="color-box" style="background-color: #f0f0f0"></span>
          <span class="color-box" style="background-color: #ebedf0"></span>
          <span class="color-box" style="background-color: #c6e48b"></span>
          <span class="color-box" style="background-color: #7bc96f"></span>
          <span class="color-box" style="background-color: #216e39"></span>
          <span class="label">All Done</span>
        </div>

        <transition name="fade">
          <div v-if="selectedTasks.length" class="task-box">
            <div class="task-header">
              <h3>Tasks for {{ selectedDate }}</h3>
              <span class="close-btn" @click="closeTasks">✖</span>
            </div>
            <ul>
              <li v-for="(task, index) in selectedTasks" :key="index">
                <span>
                  <template v-if="selectedDate < today">
                    {{ task.status === 'completed' ? '✅ Done' : '❌ Not Completed' }}
                  </template>
                  <template v-else-if="selectedDate === today">
                    {{ task.status === 'completed' ? '✅ Done' : '🟡 Pending' }}
                  </template>
                  <template v-else>
                    ⚪ Upcoming
                  </template>
                </span>
                {{ ' - ' + task.title }}
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
const calendarOptions = ref(null)
const accessToken = localStorage.getItem('access_token')

function closeTasks() {
  selectedTasks.value = []
  selectedDate.value = ''
}

// Fetch calendar report and set up calendar
const fetchCalendarReport = async () => {
  try {
    const res = await fetch('http://localhost:5000/calendar-report', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to fetch calendar report')

    const progress = data.progress
    const events = Object.entries(progress).map(([date, detail]) => ({
      title: '', // empty title to reduce clutter
      date,
      backgroundColor: detail.status,
      borderColor: detail.status,
      extendedProps: {
        not_done: detail.not_done
      }
    }))

    calendarOptions.value = {
      plugins: [dayGridPlugin],
      initialView: 'dayGridMonth',
      contentHeight: 320,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: ''
      },
      events,
      eventClick(info) {
        selectedDate.value = info.event.startStr
        const notDone = info.event.extendedProps.not_done || []
        const allTasks = ['todo', 'journal', 'story', 'infotainment']
        selectedTasks.value = allTasks
          .map(task => ({
            title: task,
            status: notDone.includes(task) ? 'not_completed' : 'completed'
          }))
          .sort((a, b) => {
            // not_completed comes before completed
            if (a.status === 'not_completed' && b.status === 'completed') return -1
            if (a.status === 'completed' && b.status === 'not_completed') return 1
            return 0
          })

      },
      eventBackgroundColor: 'transparent'
    }
  } catch (error) {
    alert(error.message)
  }
}

onMounted(() => {
  if (!accessToken) {
    alert('Please login to access calendar.')
    router.push('/login')
  }
  fetchCalendarReport()
})
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.child-calendar-bg {
  font-family: 'Comic Neue', cursive;
  display: flex;
  justify-content: center;
  padding: 0rem 1rem;
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
  border-radius: 20px;
}

.calendar-container h1 {
  font-family: 'Fredoka One', cursive;
  color: #756bdb;
  text-align: center;
  margin-bottom: 1.5rem;
}

.calendar-title {
  display: flex;
  align-items: center; 
  justify-content: center; 
  gap: 8px; 
}

.cal-icon {
  width: 40px;
  height: 100px;
  fill: #756bdb; 
}

.fc {
  font-size: 14px;
}

.fc .fc-toolbar-title {
  font-size: 1.2rem;
  font-family: 'Fredoka One', cursive;
  color: #5A4FCF;
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
  border: 1px solid #5A4FCF;
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
  color: #5A4FCF;
  font-family: 'Fredoka One', cursive;
  margin: 0;
}

.close-btn {
  font-size: 1.2rem;
  cursor: pointer;
  color: #5A4FCF;
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

.legend {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1.5rem;
  font-size: 0.85rem;
  gap: 6px;
}

.label {
  color: #888;
  font-weight: 500;
}

.color-box {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  border: 1px solid #ddd;
}
</style>