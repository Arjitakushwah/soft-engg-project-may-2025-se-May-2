<template>
  <div class="parent-calendar-bg">
    <main class="main-content">
      <div class="calendar-container">
        <!-- Child Selector -->
        <div class="child-select">
          <label for="child">Select Child:</label>
          <select id="child" v-model="selectedChild">
            <option v-for="child in children" :key="child" :value="child">{{ child }}</option>
          </select>
        </div>

        <h2>{{ selectedChild }}'s Calendar Report</h2>
        <FullCalendar :options="calendarOptions" />

        <!-- Task Modal -->
        <div v-if="showModal" class="modal-overlay">
          <div class="modal-content">
            <h3>Tasks for {{ selectedDate }}</h3>
            <ul>
              <li v-for="(task, index) in selectedTasks" :key="index">
                <span v-if="selectedDate < today">{{ task.status === 'completed' ? '✅' : '❌' }}</span>
                <span v-else-if="selectedDate === today">🟡</span>
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
import { ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

const children = ['Anya', 'Ravi', 'Meera']
const selectedChild = ref(children[0])
const selectedDate = ref('')
const selectedTasks = ref([])
const showModal = ref(false)

const today = new Date().toISOString().split('T')[0]

// Dummy event data
const rawEvents = [
  { title: 'English Essay', date: '2025-06-21', status: 'completed' },
  { title: 'Math Homework', date: '2025-06-22', status: 'pending' },
  { title: 'Science Project', date: '2025-06-23', status: 'not_completed' },
  { title: 'Art Class', date: '2025-06-24', status: 'pending' }
]

const groupedDates = [...new Set(rawEvents.map(e => e.date))]
const simplifiedEvents = groupedDates.map(date => ({
  title: 'Tasks',
  date,
  status: 'grouped'
}))

function closeModal() {
  showModal.value = false
  selectedDate.value = ''
  selectedTasks.value = []
}

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  initialDate: '2025-06-01',
  contentHeight: 350,
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
    showModal.value = true
  }
})
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

</style>
