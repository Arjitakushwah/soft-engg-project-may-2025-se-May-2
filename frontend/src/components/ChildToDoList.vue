<template>
  <div class="todo-page">
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div class="top-controls">
      <div class="date-nav">
        <button @click="goToPreviousDay" class="nav-arrow">&lt;</button>
        <span class="date-text">{{ formattedDate }}</span>
        <button @click="goToNextDay" class="nav-arrow">&gt;</button>
      </div>
      <input 
        v-model="newTask" 
        placeholder="Add new Task" 
        class="task-input" 
        @keyup.enter="addTask" 
        :disabled="!isCurrentDateToday" 
      />
    </div>
    
    <p class="task-title">Tasks</p>
    
    <div v-if="loading" class="loading">Loading tasks...</div>
    <div v-else>
      <div v-if="currentTasks.length === 0" class="no-tasks">
        No tasks for this date
      </div>
      <div v-for="(task, index) in currentTasks" :key="task.id" class="task-row">
        <span :class="['task-name', { completed: task.is_done }]">{{ task.task }}</span>
        <div class="actions">
          <button 
            v-if="!task.is_done" 
            class="btn complete" 
            @click="markCompleted(task.id)" 
            :disabled="!isCurrentDateToday"
          >
            Complete
          </button>
          <button 
            v-if="!task.is_done" 
            class="btn edit" 
            @click="editTask(task.id, task.task)" 
            :disabled="!isCurrentDateToday"
          >
            Edit
          </button>
          <button 
            class="btn delete" 
            @click="deleteTask(task.id)" 
            :disabled="!isCurrentDateToday || task.is_done"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Task Modal -->
    <div v-if="editingTask" class="modal-overlay" @click="cancelEdit">
      <div class="modal-content" @click.stop>
        <h3>Edit Task</h3>
        <input 
          v-model="editTaskText" 
          class="edit-input" 
          @keyup.enter="saveEditTask"
          placeholder="Edit task description"
        />
        <div class="modal-actions">
          <button @click="saveEditTask" class="btn save">Save</button>
          <button @click="cancelEdit" class="btn cancel">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue';

const API_BASE_URL = 'http://127.0.0.1:5000/';

// Helper functions
const formatDateKey = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const formatDisplayDate = (date) =>
  date.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });

const isToday = (date) => {
  const today = new Date();
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
};

// Reactive state
const currentDate = ref(new Date());
const newTask = ref('');
const loading = ref(false);
const error = ref(null);
const taskMap = reactive({});
const editingTask = ref(null);
const editTaskText = ref('');

// Computed properties
const formattedDate = computed(() => formatDisplayDate(currentDate.value));
const isCurrentDateToday = computed(() => isToday(currentDate.value));
const currentTasks = computed(() => {
  const key = formatDateKey(currentDate.value);
  return taskMap[key] || [];
});

// API functions using fetch
async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem('access_token'); // Changed from 'token' to 'access_token'
  if (!token) {
    error.value = 'Please login first';
    throw new Error('No token found');
  }

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    ...options.headers
  };

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Request failed');
  }

  return response.json();
}

async function loadTasksForDate(date) {
  const queryDate = formatDateKey(date);
  
  if (taskMap[queryDate]) return; // Already loaded
  
  loading.value = true;
  error.value = null;
  
  try {
    const data = await fetchWithAuth(`${API_BASE_URL}/todo?date=${queryDate}`);
    taskMap[queryDate] = data.tasks; // Backend returns tasks array directly
  } catch (err) {
    error.value = err.message || 'Failed to load tasks';
    console.error('Error loading tasks:', err);
  } finally {
    loading.value = false;
  }
}

async function addTask() {
  const key = formatDateKey(currentDate.value);
  
  if (!newTask.value.trim()) {
    error.value = 'Task cannot be empty';
    return;
  }

  try {
    const data = await fetchWithAuth(`${API_BASE_URL}/todo`, {
      method: 'POST',
      body: JSON.stringify({
        task: newTask.value.trim(),
        date: key
      })
    });

    // Reload tasks for the current date after adding
    delete taskMap[key]; // Clear cache
    await loadTasksForDate(currentDate.value);
    
    newTask.value = '';
    error.value = null;
  } catch (err) {
    error.value = err.message || 'Failed to add task';
    console.error('Error adding task:', err);
  }
}

async function markCompleted(taskId) {
  try {
    await fetchWithAuth(`${API_BASE_URL}/todo/status/${taskId}`, {
      method: 'PUT'
    });
    
    // Update the task in the local state
    const key = formatDateKey(currentDate.value);
    const taskIndex = taskMap[key].findIndex(t => t.id === taskId);
    if (taskIndex !== -1) {
      taskMap[key][taskIndex].is_done = true;
    }
    
    error.value = null;
  } catch (err) {
    error.value = err.message || 'Failed to complete task';
    console.error('Error completing task:', err);
  }
}

async function deleteTask(taskId) {
  try {
    await fetchWithAuth(`${API_BASE_URL}/todo/${taskId}`, {
      method: 'DELETE'
    });
    
    // Remove task from local state
    const key = formatDateKey(currentDate.value);
    const taskIndex = taskMap[key].findIndex(t => t.id === taskId);
    if (taskIndex !== -1) {
      taskMap[key].splice(taskIndex, 1);
    }
    
    error.value = null;
  } catch (err) {
    error.value = err.message || 'Failed to delete task';
    console.error('Error deleting task:', err);
  }
}

async function editTask(taskId, taskText) {
  editingTask.value = taskId;
  editTaskText.value = taskText;
}

async function saveEditTask() {
  if (!editTaskText.value.trim()) {
    error.value = 'Task cannot be empty';
    return;
  }

  try {
    await fetchWithAuth(`${API_BASE_URL}/todo/${editingTask.value}`, {
      method: 'PUT',
      body: JSON.stringify({
        task: editTaskText.value.trim(),
        date: formatDateKey(currentDate.value)
      })
    });

    // Update task in local state
    const key = formatDateKey(currentDate.value);
    const taskIndex = taskMap[key].findIndex(t => t.id === editingTask.value);
    if (taskIndex !== -1) {
      taskMap[key][taskIndex].task = editTaskText.value.trim();
    }

    cancelEdit();
    error.value = null;
  } catch (err) {
    error.value = err.message || 'Failed to update task';
    console.error('Error updating task:', err);
  }
}

function cancelEdit() {
  editingTask.value = null;
  editTaskText.value = '';
}

// Navigation functions
function goToPreviousDay() {
  const newDate = new Date(currentDate.value);
  newDate.setDate(newDate.getDate() - 1);
  currentDate.value = newDate;
  loadTasksForDate(newDate);
}

function goToNextDay() {
  const newDate = new Date(currentDate.value);
  newDate.setDate(newDate.getDate() + 1);
  currentDate.value = newDate;
  loadTasksForDate(newDate);
}

// Initialize
onMounted(() => {
  loadTasksForDate(currentDate.value);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.todo-page {
  padding: 2rem;
  font-family: 'Comic Neue', cursive;
  min-height: 100vh;
  background: #f9f9f9;
}

.error-message {
  color: #dc3545;
  padding: 0.8rem;
  margin-bottom: 1rem;
  background: #ffe6e6;
  border-radius: 8px;
  text-align: center;
}

.top-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
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
  font-size: 1.3rem;
  color: #ff6a88;
  min-width: 180px;
  text-align: center;
}

.nav-arrow {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #1e3a8a;
  cursor: pointer;
  padding: 0.3rem 0.8rem;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.nav-arrow:hover {
  background-color: #f0f0f0;
}

.task-input {
  flex: 1;
  min-width: 200px;
  padding: 0.7rem 1rem;
  border: 2px solid #ff6a88;
  border-radius: 10px;
  background: #fff;
  font-family: 'Comic Neue', cursive;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.task-input:focus {
  outline: none;
  border-color: #1e3a8a;
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
  background: #fff;
  border-left: 5px solid #ff6a88;
  padding: 1rem 1.5rem;
  margin-bottom: 0.8rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.task-row:hover {
  transform: translateY(-2px);
}

.task-name {
  flex: 1;
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}

.task-name.completed {
  text-decoration: line-through;
  color: #888;
}

.actions {
  display: flex;
  gap: 0.8rem;
}

.btn {
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  font-family: 'Comic Neue', cursive;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:not(:disabled):hover {
  transform: scale(1.05);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.complete {
  background-color: #28a745;
  color: white;
}

.edit {
  background-color: #17a2b8;
  color: white;
}

.delete {
  background-color: #fd466e;
  color: white;
}

.save {
  background-color: #28a745;
  color: white;
}

.cancel {
  background-color: #6c757d;
  color: white;
}

.loading {
  text-align: center;
  padding: 1rem;
  color: #666;
}

.no-tasks {
  text-align: center;
  padding: 1rem;
  color: #888;
  font-style: italic;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  min-width: 400px;
  max-width: 90vw;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-family: 'Fredoka One', cursive;
  color: #333;
}

.edit-input {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 2px solid #ff6a88;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-family: 'Comic Neue', cursive;
  font-size: 1rem;
}

.edit-input:focus {
  outline: none;
  border-color: #1e3a8a;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
</style>