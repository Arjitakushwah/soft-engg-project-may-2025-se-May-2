<template>
  <div class="parent-calendar-bg">
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

          <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
              <h3>Tasks for {{ selectedDate }}</h3>
              <ul>
                <li v-for="(task, index) in selectedTasks" :key="index"
                  :class="getStatusClass(task.status, selectedDate)">
                  {{ task.title }}
                </li>

              </ul>
              <button @click="closeModal" class="close-btn">Close</button>
            </div>
          </div>
        
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
const showModal = ref(false)
const today = new Date().toISOString().split('T')[0]
const calendarOptions = ref(null)

const accessToken = localStorage.getItem('access_token')

// Get child name by ID
function getChildName(id) {
  const child = children.value.find(c => c.id === id)
  return child ? child.name : ''
}

// Fetch child list
const fetchChildren = async () => {
  try {
    const response = await fetch('http://localhost:5000/parent/children', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })

    if (!response.ok) throw new Error('Unauthorized or failed to fetch children.')

    const data = await response.json()
    children.value = data.children
    if (children.value.length > 0) {
      selectedChild.value = children.value[0].id
    }
  } catch (err) {
    alert(err.message)
  }
}

// Fetch calendar report for a selected child
const fetchCalendarReport = async (childId) => {
  try {
    const response = await fetch(`http://localhost:5000/parent/child/${childId}/calendar-report`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })

    if (!response.ok) throw new Error('Failed to fetch calendar report.')

    const data = await response.json()
    const report = data.report

    const events = Object.entries(report).map(([date, details]) => ({
      title: `✅ ${details.total_completed}/4`,
      date,
      extendedProps: {
        completed: details.completed,
        not_completed: details.not_completed
      }
    }))

    calendarOptions.value = {
      plugins: [dayGridPlugin],
      initialView: 'dayGridMonth',
      contentHeight: 350,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: ''
      },
      events,
      eventContent(arg) {
        return {
          html: `<div style="color: black; font-weight: bold;">${arg.event.title}</div>`
        }
      },
      eventClick(info) {
        selectedDate.value = info.event.startStr
        const tasks = ['todo', 'journal', 'story', 'infotainment']
        const completed = info.event.extendedProps.completed || []

        selectedTasks.value = tasks.map(task => ({
          title: task,
          status: completed.includes(task) ? 'completed' : 'not_completed'
        }))

        showModal.value = true
      }
    }
  } catch (err) {
    alert(err.message)
  }
}

// React to child selection
watch(selectedChild, (newVal) => {
  if (newVal) fetchCalendarReport(newVal)
})

// Load children on component mount
onMounted(() => {
  if (!accessToken) {
    alert('You must be logged in as parent.')
    return
  }
  fetchChildren()
})

function closeModal() {
  showModal.value = false
  selectedDate.value = ''
  selectedTasks.value = []
}

function getStatusClass(status, date) {
  if (status === 'completed') {
    return 'task-completed'
  } else {
    if (date === today) return 'task-pending-today'
    if (date < today) return 'task-missed'
  }
  return ''
}

</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.parent-calendar-bg {
  font-family: 'Comic Neue', cursive;


  color: #333;
  display: flex;
  flex-direction: column;
}

.main-content {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  min-height: calc(100vh - 100px);
}

.calendar-container {
  background: white;
  padding: 20px;
  width: 90%;
  max-width: 800px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
}

.child-select {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Comic Neue', cursive;
  font-size: 16px;
}

.child-select select {
  padding: 6px 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.fc {
  font-size: 14px;
}

.fc-event {
  pointer-events: auto;
  /* ensure it's clickable */
}


.fc .fc-toolbar-title {
  font-size: 1.4rem;
  font-family: 'Fredoka One', cursive;
  color: #3b82f6;
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
  max-width: 90%;
}

.task-box {
  margin-top: 1.5rem;
  background: #ffe6ec;
  border: 1px solid #ff6a88;
  box-shadow: 0 2px 8px rgba(255, 106, 136, 0.08);
  border-radius: 12px;
  font-size: 15px;
  padding: 12px;
}

.task-box h3 {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  color: #ff6a88;
  font-family: 'Fredoka One', cursive;
}

.task-box ul {
  list-style-type: none;
  padding-left: 0;
}

.task-box li {
  margin: 0.5rem 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background-color: white;
  padding: 20px 30px;
  border-radius: 12px;
  width: 350px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  font-size: 16px;
  position: relative;
  font-family: 'Comic Neue', cursive;
}

.modal-content h3 {
  font-family: 'Fredoka One', cursive;
  font-size: 1.2rem;
  color: #ff6a88;
  margin-bottom: 1rem;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
}

.modal-content li {
  margin: 0.5rem 0;
}

.close-btn {
  margin-top: 15px;
  background-color: #ff6a88;
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
  font-family: 'Comic Neue', cursive;
  cursor: pointer;
}

.task-completed {
  background-color: #d4f4dd;
  /* light green */
  color: #2e7d32;
  /* dark green */
  padding: 6px 10px;
  border-radius: 8px;
  font-weight: bold;
}

.task-pending-today {
  background-color: #fff8dc;
  /* light yellow */
  color: #ff9800;
  /* orange */
  padding: 6px 10px;
  border-radius: 8px;
  font-weight: bold;
}

.task-missed {
  background-color: #ffe6e6;
  /* light red */
  color: #d32f2f;
  /* dark red */
  padding: 6px 10px;
  border-radius: 8px;
  font-weight: bold;
}
</style>
