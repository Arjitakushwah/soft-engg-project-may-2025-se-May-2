<template>
  <div class="child-calendar-bg">
    <main class="main-content">
      <div class="calendar-container">
        <div class="child-select" v-if="children.length > 0">
          <label for="child">Select Child:</label>
          <select id="child" v-model="selectedChild">
            <option v-for="child in children" :key="child.id" :value="child.id">
              {{ child.name }}
            </option>
          </select>
        </div>

        <p v-else style="margin-top: 1rem; color: #e11d48; font-weight: bold;">
          No children added to your account.
        </p>

        <h2 v-if="selectedChild">
          {{ getChildName(selectedChild) }}'s Calendar Report
        </h2>

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
              <span class="close-btn" @click="closeModal">✖</span>
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

const router = useRouter()
const children = ref([])
const selectedChild = ref(null)
const selectedDate = ref('')
const selectedTasks = ref([])
const today = new Date().toISOString().split('T')[0]
const calendarOptions = ref(null)
const accessToken = localStorage.getItem('access_token')

function getChildName(id) {
  const child = children.value.find(c => c.id === id)
  return child ? child.name : ''
}

function closeModal() {
  selectedTasks.value = []
  selectedDate.value = ''
}

const fetchChildren = async () => {
  try {
    const response = await fetch('http://localhost:5000/parent/children', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.error || 'Failed to fetch children.')
    children.value = data.children
    if (children.value.length > 0) {
      selectedChild.value = children.value[0].id
    }
  } catch (err) {
    alert(err.message)
  }
}

const fetchCalendarReport = async (childId) => {
  try {
    const response = await fetch(`http://localhost:5000/parent/child/${childId}/calendar-report`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })

    const data = await response.json()
    if (!response.ok) throw new Error(data.error || 'Failed to fetch calendar report')

    const report = data.report

    const events = Object.entries(report).map(([date, details]) => {
      const level = details.total_completed || 0
      const statusColors = ['#f0f0f0', '#ebedf0', '#c6e48b', '#7bc96f', '#216e39']
      return {
        title: '',
        date,
        backgroundColor: statusColors[level],
        borderColor: statusColors[level],
        extendedProps: {
          completed: details.completed || []
        }
      }
    })

    calendarOptions.value = {
      plugins: [dayGridPlugin],
      initialView: 'dayGridMonth',
      initialDate: today,
      contentHeight: 400,
      contentWidth: '100%',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: ''
      },
      events,
      eventClick(info) {
        selectedDate.value = info.event.startStr
        const completed = info.event.extendedProps.completed || []
        const tasks = ['todo', 'journal', 'story', 'infotainment']
        selectedTasks.value = tasks.map(task => ({
          title: task,
          status: completed.includes(task) ? 'completed' : 'not_completed'
        }))
      },
      eventBackgroundColor: 'transparent'
    }
  } catch (err) {
    alert(err.message)
  }
}

watch(selectedChild, (newVal) => {
  if (newVal) fetchCalendarReport(newVal)
})

onMounted(() => {
  if (!accessToken) {
    alert('Please log in as a parent.')
    router.push('/login')
  }
  fetchChildren()
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
  max-width: 1000px;
  height: 100%;
  display: flex;
  justify-content: center;
}

.calendar-container {
  background: #fff;
  padding: 2rem;
  width: 100%;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.calendar-container h2 {
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  text-align: center;
  margin-bottom: 1.5rem;
}

.child-select {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}

.child-select select {
  padding: 6px 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.fc .fc-toolbar-title {
  font-size: 1.2rem;
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
}

.fc-daygrid-day-number {
  font-size: 0.9rem;
}

.fc-daygrid-event {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.fc-day {
  background: #8d1b32 !important ;
  color: #fff;
  font-family: 'Fredoka One', cursive;
  font-size: 1.1rem;
}
.fc-daygrid-day-top {
  font-family: 'Comic Neue', cursive;
  font-weight: bold;
  color: #333 !important;
}

/* Today cell highlight */
.fc-day-today {
  background-color: #ffe3ec !important;
}

/* Day cell hover effect */
.fc-daygrid-day:hover {
  background-color: #fff5f7 !important;
  cursor: pointer;
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
