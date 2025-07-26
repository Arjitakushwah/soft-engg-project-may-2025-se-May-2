<template> 
  <div class="todo-app"> 
    <div class="app-header"> 
      <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
        <path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1s-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/> 
      </svg> 
      <h1>My Awesome To-Do List</h1> 
    </div> 

    <div v-if="error" class="error-message"> 
      <svg class="error-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/> 
      </svg> 
      {{ error }} 
    </div> 

    <div v-if="showCongratulations" class="celebration-banner"> 
      <svg class="celebration-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
        <path d="M12 2L8 7l-7 3 5 6-1 7 7-3 7 3-1-7 5-6-7-3-4-5z"/> 
      </svg> 
      <span>Awesome! Task Completed!</span> 
      <svg class="celebration-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
        <path d="M12 2L8 7l-7 3 5 6-1 7 7-3 7 3-1-7 5-6-7-3-4-5z"/> 
      </svg> 
    </div> 

    <div class="date-navigation"> 
      <button @click="goToPreviousDay" class="nav-button"> 
        <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/> 
        </svg> 
      </button> 
      <div class="current-date"> 
        <svg class="date-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/> 
        </svg> 
        <span>{{ formattedDate }}</span> 
      </div> 
      <button @click="goToNextDay" class="nav-button"> 
        <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/> 
        </svg> 
      </button> 
    </div> 

    <div class="task-creator"> 
      <div class="input-group"> 
        <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/> 
        </svg> 
        <input  
          v-model="newTask"  
          placeholder="What do you need to do?"  
          class="task-input" 
          @keyup.enter="addTask" 
          :disabled="!isCurrentDateToday" 
        /> 
      </div> 
      <div class="time-selectors"> 
        <div class="time-input"> 
          <svg class="time-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
            <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/> 
            <path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z"/> 
          </svg> 
          <input 
            v-model="taskTime" 
            type="time" 
            class="time-field" 
            :disabled="!isCurrentDateToday" 
          /> 
        </div> 
        <div class="date-input"> 
          <svg class="date-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
            <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/> 
          </svg> 
          <input  
            v-model="taskDate" 
            type="date" 
            class="date-field" 
            :min="minDate" 
            :disabled="!isCurrentDateToday" 
          /> 
        </div> 
      </div> 
      <button  
        @click="addTask"  
        class="add-button" 
        :disabled="!isCurrentDateToday || !newTask.trim()" 
      > 
        <svg class="add-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/> 
        </svg> 
        Add Task 
      </button> 
    </div> 

    <div class="tasks-section"> 
      <h2 class="section-title"> 
        <svg class="section-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/> 
        </svg> 
        Today's Tasks 
      </h2> 

      <div v-if="loading" class="loading-state"> 
        <svg class="spinner" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
          <path d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z"> 
            <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/> 
          </path> 
        </svg> 
        Loading your tasks... 
      </div> 

      <div v-else> 
        <div v-if="currentTasks.length === 0" class="empty-state"> 
          <svg class="empty-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/> 
            <path d="M12 7c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 5c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/> 
          </svg> 
          <p>No tasks for today! Add one above!</p> 
        </div> 
        
        <!-- ✅ NEW: Added a grid container for the tasks -->
        <div v-else class="task-grid">
            <div v-for="(task) in sortedTasks" :key="task.id" class="task-card" :class="{ completed: task.is_done }"> 
              <div class="task-content"> 
                <div class="task-text"> 
                  <span class="task-name">{{ task.task }}</span> 
                  <span class="task-time" v-if="task.time"> 
                    <svg class="time-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
                      <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/> 
                      <path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z"/> 
                    </svg> 
                    {{ formatTime(task.time) }} 
                  </span> 
                </div> 
                <div class="task-actions"> 
                  <button  
                    v-if="!task.is_done && isCurrentDateToday"  
                    class="action-button complete"  
                    @click="markCompleted(task.id)" 
                    title="Complete" 
                  > 
                    <svg class="action-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
                      <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/> 
                    </svg> 
                  </button> 
                  <button  
                    v-if="!task.is_done && isCurrentDateToday"  
                    class="action-button edit"  
                    @click="editTask(task.id, task.task, task.date, task.time)" 
                    title="Edit" 
                  > 
                    <svg class="action-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
                      <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/> 
                    </svg> 
                  </button> 
                  <button  
                    class="action-button delete"  
                    @click="deleteTask(task.id)"  
                    :disabled="!isCurrentDateToday || task.is_done" 
                    title="Delete" 
                  > 
                    <svg class="action-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
                      <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/> 
                    </svg> 
                  </button> 
                </div> 
              </div> 
            </div>
        </div>
      </div> 
    </div> 

    <div v-if="editingTask" class="modal-overlay" @click.self="cancelEdit"> 
      <div class="modal-content" @click.stop> 
        <h3 class="modal-title"> 
          <svg class="modal-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
            <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/> 
          </svg> 
          Edit Task 
        </h3> 
        <div class="modal-input-group"> 
          <svg class="modal-input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/> 
          </svg> 
          <input  
            v-model="editTaskText"  
            class="modal-input"  
            placeholder="Task description" 
          /> 
        </div> 
        <div class="modal-time-selectors"> 
          <div class="modal-time-input"> 
            <svg class="modal-time-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
              <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/> 
              <path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z"/> 
            </svg> 
            <input 
              v-model="editTaskTime" 
              type="time" 
              class="modal-time-field" 
            /> 
          </div> 
          <div class="modal-date-input"> 
            <svg class="modal-date-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
              <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/> 
            </svg> 
            <input  
              v-model="editTaskDate" 
              type="date" 
              class="modal-date-field" 
              :min="minDate" 
            /> 
          </div> 
        </div> 
        <div class="modal-actions"> 
          <button @click="saveEditTask" class="modal-button save"> 
            <svg class="modal-button-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
              <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/> 
            </svg> 
            Save 
          </button> 
          <button @click="cancelEdit" class="modal-button cancel"> 
            <svg class="modal-button-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> 
              <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/> 
            </svg> 
            Cancel 
          </button> 
        </div> 
      </div> 
    </div> 
  </div> 
</template> 

<script setup> 
import { ref, computed, reactive, onMounted } from 'vue'; 

const API_BASE_URL = 'http://127.0.0.1:5000'; 

const currentDate = ref(new Date()); 
const newTask = ref(''); 
const taskDate = ref(''); 
const taskTime = ref('12:00'); 
const editTaskDate = ref(''); 
const editTaskTime = ref('12:00'); 
const loading = ref(false); 
const error = ref(null); 
const taskMap = reactive({}); 
const editingTask = ref(null); 
const editTaskText = ref(''); 
const showCongratulations = ref(false); 

// Helper functions 
const formatDateKey = (date) => { 
  const d = new Date(date); 
  // Adjust for timezone offset to prevent the date from changing
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().split('T')[0]; 
}; 

const formatDisplayDate = (date) => { 
  const options = { day: 'numeric', month: 'long', year: 'numeric' }; 
  return new Date(date).toLocaleDateString('en-GB', options); 
}; 

const formatTime = (timeString) => { 
  if (!timeString) return ''; 
  const [hours, minutes] = timeString.split(':'); 
  const hour = parseInt(hours); 
  const ampm = hour >= 12 ? 'PM' : 'AM'; 
  const displayHour = hour % 12 || 12; 
  return `${displayHour}:${minutes} ${ampm}`; 
}; 

const isToday = (date) => { 
  const now = new Date(); 
  const compareDate = new Date(date); 
  return compareDate.getDate() === now.getDate() && 
         compareDate.getMonth() === now.getMonth() && 
         compareDate.getFullYear() === now.getFullYear(); 
}; 

// Computed properties 
const formattedDate = computed(() => formatDisplayDate(currentDate.value)); 
const isCurrentDateToday = computed(() => isToday(currentDate.value)); 
const currentTasks = computed(() => { 
  const key = formatDateKey(currentDate.value); 
  return taskMap[key] || []; 
}); 

const sortedTasks = computed(() => { 
  return [...currentTasks.value].sort((a, b) => { 
    if (a.is_done !== b.is_done) { 
      return a.is_done - b.is_done; 
    } 
    if (!a.time || !b.time) return 0; 
    return a.time.localeCompare(b.time); 
  }); 
}); 

const minDate = computed(() => { 
  const today = new Date(); 
  return today.toISOString().split('T')[0]; 
}); 

// API functions 
async function fetchWithAuth(url, options = {}) { 
  const token = localStorage.getItem('access_token'); 
  if (!token) throw new Error('Please login first'); 

  const headers = { 
    'Content-Type': 'application/json', 
    'Authorization': `Bearer ${token}`, 
    ...options.headers 
  }; 

  const response = await fetch(url, { ...options, headers }); 
  const data = await response.json().catch(() => ({})); 
  if (!response.ok) throw new Error(data.error || 'Request failed'); 
  return data; 
} 

async function loadTasksForDate(date, force = false) { 
  const key = formatDateKey(date); 
  if (taskMap[key] && !force) {
    return;
  }

  loading.value = true; 
  error.value = null;
  try { 
    const data = await fetchWithAuth(`${API_BASE_URL}/todo?date=${key}`); 
    taskMap[key] = data.tasks; 
  } catch (err) { 
    error.value = err.message; 
    taskMap[key] = []; 
  } finally { 
    loading.value = false; 
  } 
} 

async function addTask() { 
  if (!newTask.value.trim()) { 
    error.value = 'Task cannot be empty'; 
    return; 
  } 

  try { 
    const dateToSend = taskDate.value || formatDateKey(currentDate.value);
    const created = await fetchWithAuth(`${API_BASE_URL}/todo`, { 
      method: 'POST', 
      body: JSON.stringify({  
        task: newTask.value.trim(),  
        date: dateToSend, 
        time: taskTime.value 
      }) 
    }); 

    const createdTaskDate = new Date(created.date);
    const adjustedDate = new Date(createdTaskDate.getTime() + createdTaskDate.getTimezoneOffset() * 60000);
    await loadTasksForDate(adjustedDate, true);

    newTask.value = ''; 
    taskDate.value = minDate.value; 
    taskTime.value = '12:00'; 
    error.value = null; 
  } catch (err) { 
    error.value = err.message; 
  } 
} 

async function markCompleted(taskId) { 
  try { 
    await fetchWithAuth(`${API_BASE_URL}/todo/status/${taskId}`, { method: 'PUT' }); 
    
    showCongratulations.value = true; 
    setTimeout(() => { 
      showCongratulations.value = false; 
    }, 3000); 

    await loadTasksForDate(currentDate.value, true);
  } catch (err) { 
    error.value = err.message; 
  } 
} 

async function deleteTask(taskId) { 
  try { 
    await fetchWithAuth(`${API_BASE_URL}/todo/${taskId}`, { method: 'DELETE' }); 
    await loadTasksForDate(currentDate.value, true);
  } catch (err) { 
    error.value = err.message; 
  } 
} 

function editTask(taskId, text, date, time) { 
  editingTask.value = taskId; 
  editTaskText.value = text; 
  editTaskDate.value = date; 
  editTaskTime.value = time || '12:00'; 
} 

async function saveEditTask() { 
  if (!editTaskText.value.trim()) { 
    error.value = 'Task cannot be empty'; 
    return; 
  } 

  try { 
    const newDateKey = editTaskDate.value || formatDateKey(currentDate.value);
    await fetchWithAuth(`${API_BASE_URL}/todo/${editingTask.value}`, { 
      method: 'PUT', 
      body: JSON.stringify({ 
        task: editTaskText.value.trim(), 
        date: newDateKey, 
        time: editTaskTime.value 
      }) 
    }); 

    await loadTasksForDate(currentDate.value, true);

    if (newDateKey !== formatDateKey(currentDate.value)) {
        delete taskMap[newDateKey];
    }

    cancelEdit(); 
  } catch (err) { 
    error.value = err.message; 
  } 
} 

function cancelEdit() { 
  editingTask.value = null; 
  editTaskText.value = ''; 
  editTaskDate.value = ''; 
  editTaskTime.value = '12:00'; 
} 

function goToPreviousDay() { 
  const d = new Date(currentDate.value); 
  d.setDate(d.getDate() - 1); 
  currentDate.value = d; 
  loadTasksForDate(d); 
} 

function goToNextDay() { 
  const d = new Date(currentDate.value); 
  d.setDate(d.getDate() + 1); 
  currentDate.value = d; 
  loadTasksForDate(d); 
} 

onMounted(() => { 
  taskDate.value = minDate.value; 
  loadTasksForDate(currentDate.value); 
}); 
</script> 

<style scoped> 
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Fredoka+One&display=swap'); 

.todo-app { 
  /* ✅ CHANGED: Increased max-width for a wider layout on large screens */
  max-width: 960px; 
  margin: 0 auto; 
  padding: 1.5rem; 
  font-family: 'Comic Neue', cursive; 
  background-color: #f9f9f9; 
  min-height: 100vh; 
} 

.app-header { 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 1rem; 
  margin-bottom: 2rem; 
  color: #4f46e5; 
} 

.app-header h1 { 
  font-family: 'Fredoka One', cursive; 
  font-size: 2rem; 
  margin: 0; 
} 

.header-icon { 
  width: 40px; 
  height: 40px; 
  fill: currentColor; 
} 

.error-message { 
  background-color: #fee2e2; 
  color: #b91c1c; 
  padding: 1rem; 
  border-radius: 12px; 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  margin-bottom: 1.5rem; 
  font-weight: bold; 
} 

.error-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; 
} 

.celebration-banner { 
  background-color: #d1fae5; 
  color: #065f46; 
  padding: 1rem; 
  border-radius: 12px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 1rem; 
  margin-bottom: 1.5rem; 
  font-weight: bold; 
  animation: bounce 0.5s ease-in-out; 
} 

@keyframes bounce { 
  0%, 100% { transform: translateY(0); } 
  50% { transform: translateY(-10px); } 
} 

.celebration-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; 
} 

.date-navigation { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  margin-bottom: 1.5rem; 
  background-color: #e0e7ff; 
  padding: 0.75rem; 
  border-radius: 12px; 
} 

.nav-button { 
  background-color: #4f46e5; 
  color: white; 
  border: none; 
  border-radius: 8px; 
  width: 40px; 
  height: 40px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  cursor: pointer; 
  transition: transform 0.2s; 
} 

.nav-button:hover { 
  transform: scale(1.1); 
} 

.nav-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; 
} 

.current-date { 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  font-family: 'Fredoka One', cursive; 
  font-size: 1.2rem; 
  color: #4f46e5; 
} 

.date-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; 
} 

.task-creator { 
  background-color: white; 
  padding: 1.5rem; 
  border-radius: 16px; 
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); 
  margin-bottom: 2rem; 
} 

.input-group { 
  position: relative; 
  margin-bottom: 1rem; 
} 

.input-icon { 
  position: absolute; 
  left: 12px; 
  top: 50%; 
  transform: translateY(-50%); 
  width: 20px; 
  height: 20px; 
  fill: #64748b; 
} 

.task-input { 
  width: 100%; 
  padding: 0.75rem 1rem 0.75rem 40px; 
  border: 2px solid #e0e7ff; 
  border-radius: 12px; 
  font-size: 1rem; 
  font-family: 'Comic Neue', cursive; 
  transition: border-color 0.2s; 
} 

.task-input:focus { 
  outline: none; 
  border-color: #4f46e5; 
} 

.time-selectors { 
  display: flex; 
  gap: 1rem; 
  margin-bottom: 1rem; 
} 

.time-input, .date-input { 
  position: relative; 
  flex: 1; 
} 

.time-input .time-icon,  
.date-input .date-icon { 
  position: absolute; 
  left: 12px; 
  top: 50%; 
  transform: translateY(-50%); 
  width: 20px; 
  height: 20px; 
  fill: #64748b; 
  pointer-events: none; 
} 

.time-field, .date-field { 
  width: 100%; 
  padding: 0.75rem 1rem 0.75rem 40px; 
  border: 2px solid #e0e7ff; 
  border-radius: 12px; 
  font-size: 1rem; 
  font-family: 'Comic Neue', cursive; 
} 

.add-button { 
  width: 100%; 
  padding: 0.75rem; 
  background-color: #4f46e5; 
  color: white; 
  border: none; 
  border-radius: 12px; 
  font-family: 'Fredoka One', cursive; 
  font-size: 1rem; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 0.5rem; 
  cursor: pointer; 
  transition: transform 0.2s; 
} 

.add-button:hover { 
  transform: translateY(-2px); 
} 

.add-button:disabled { 
  background-color: #c7d2fe; 
  cursor: not-allowed; 
  transform: none; 
} 

.add-icon { 
  width: 20px; 
  height: 20px; 
  fill: currentColor; 
} 

.tasks-section { 
  background-color: white; 
  padding: 1.5rem; 
  border-radius: 16px; 
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); 
} 

.section-title { 
  font-family: 'Fredoka One', cursive; 
  color: #4f46e5; 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  margin-top: 0; 
  margin-bottom: 1.5rem; 
} 

.section-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; 
} 

.loading-state { 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 0.5rem; 
  padding: 2rem; 
  color: #64748b; 
} 

.spinner { 
  width: 24px; 
  height: 24px; 
  fill: #4f46e5; 
  animation: spin 1s linear infinite; 
} 

@keyframes spin { 
  from { transform: rotate(0deg); } 
  to { transform: rotate(360deg); } 
} 

.empty-state { 
  text-align: center; 
  padding: 2rem; 
  color: #64748b; 
} 

.empty-icon { 
  width: 48px; 
  height: 48px; 
  fill: #cbd5e1; 
  margin-bottom: 1rem; 
} 

/* ✅ NEW: Styles for the responsive task grid */
.task-grid {
  display: grid;
  grid-template-columns: 1fr; /* Default to 1 column on mobile */
  gap: 1rem;
}

.task-card { 
  background-color: #f8fafc; 
  border-left: 4px solid #4f46e5; 
  border-radius: 12px; 
  padding: 1rem; 
  /* ✅ REMOVED: margin-bottom is now handled by the grid gap */
  transition: transform 0.2s; 
} 

.task-card:hover { 
  transform: translateY(-3px); 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
} 

.task-card.completed { 
  border-left-color: #10b981; 
  background-color: #ecfdf5; 
} 

.task-content { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
} 

.task-text { 
  flex: 1; 
  /* ✅ NEW: Added for better text wrapping */
  min-width: 0; 
} 

.task-name { 
  font-weight: bold; 
  display: block; 
  margin-bottom: 0.25rem; 
  color: #1e293b; 
  /* ✅ NEW: Added for better text wrapping */
  word-wrap: break-word;
} 

.task-card.completed .task-name { 
  text-decoration: line-through; 
  color: #64748b; 
} 

.task-time { 
  display: flex; 
  align-items: center; 
  gap: 0.25rem; 
  font-size: 0.875rem; 
  color: #64748b; 
} 

.task-time .time-icon { 
  width: 16px; 
  height: 16px; 
  fill: currentColor; 
} 

.task-actions { 
  display: flex; 
  gap: 0.5rem; 
} 

.action-button { 
  width: 36px; 
  height: 36px; 
  border: none; 
  border-radius: 50%; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  cursor: pointer; 
  transition: transform 0.2s; 
} 

.action-button:hover { 
  transform: scale(1.1); 
} 

.action-button:disabled { 
  opacity: 0.5; 
  cursor: not-allowed; 
  transform: none; 
} 

.action-icon { 
  width: 18px; 
  height: 18px; 
  fill: white; 
} 

.complete { 
  background-color: #10b981; 
} 

.edit { 
  background-color: #0ea5e9; 
} 

.delete { 
  background-color: #ef4444; 
} 

/* Modal styles */ 
.modal-overlay { 
  position: fixed; 
  top: 0; 
  left: 0; 
  right: 0; 
  bottom: 0; 
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 1000; 
} 

.modal-content { 
  background-color: white; 
  padding: 1.5rem; 
  border-radius: 16px; 
  width: 90%; 
  max-width: 500px; 
} 

.modal-title { 
  font-family: 'Fredoka One', cursive; 
  color: #4f46e5; 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  margin-top: 0; 
  margin-bottom: 1.5rem; 
} 

.modal-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; 
} 

.modal-input-group { 
  position: relative; 
  margin-bottom: 1rem; 
} 

.modal-input-icon { 
  position: absolute; 
  left: 12px; 
  top: 50%; 
  transform: translateY(-50%); 
  width: 20px; 
  height: 20px; 
  fill: #64748b; 
} 

.modal-input { 
  width: 100%; 
  padding: 0.75rem 1rem 0.75rem 40px; 
  border: 2px solid #e0e7ff; 
  border-radius: 12px; 
  font-size: 1rem; 
  font-family: 'Comic Neue', cursive; 
} 

.modal-time-selectors { 
  display: flex; 
  gap: 1rem; 
  margin-bottom: 1.5rem; 
} 

.modal-time-input, .modal-date-input { 
  position: relative; 
  flex: 1; 
} 

.modal-time-icon, .modal-date-icon { 
  position: absolute; 
  left: 12px; 
  top: 50%; 
  transform: translateY(-50%); 
  width: 20px; 
  height: 20px; 
  fill: #64748b; 
} 

.modal-time-field, .modal-date-field { 
  width: 100%; 
  padding: 0.75rem 1rem 0.75rem 40px; 
  border: 2px solid #e0e7ff; 
  border-radius: 12px; 
  font-size: 1rem; 
  font-family: 'Comic Neue', cursive; 
} 

.modal-actions { 
  display: flex; 
  justify-content: flex-end; 
  gap: 1rem; 
} 

.modal-button { 
  padding: 0.75rem 1.5rem; 
  border: none; 
  border-radius: 12px; 
  font-family: 'Fredoka One', cursive; 
  font-size: 1rem; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 0.5rem; 
  cursor: pointer; 
  transition: transform 0.2s; 
} 

.modal-button:hover { 
  transform: translateY(-2px); 
} 

.save { 
  background-color: #10b981; 
  color: white; 
} 

.cancel { 
  background-color: #64748b; 
  color: white; 
} 

.modal-button-icon { 
  width: 20px; 
  height: 20px; 
  fill: currentColor; 
} 

/* ✅ CHANGED: Updated responsive styles */
@media (max-width: 767px) { 
  .app-header h1 { 
    font-size: 1.5rem; 
  } 
   
  .time-selectors, .modal-time-selectors { 
    flex-direction: column; 
    gap: 0.5rem; 
  } 
   
  .task-content { 
    flex-direction: column; 
    align-items: flex-start; 
    gap: 1rem; 
  } 
   
  .task-actions { 
    align-self: flex-end; 
  } 
} 

/* ✅ NEW: Media query for the 2-column grid on wider screens */
@media (min-width: 768px) {
  .task-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
