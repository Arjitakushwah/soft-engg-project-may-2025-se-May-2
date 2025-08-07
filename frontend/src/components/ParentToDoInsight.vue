<template>
    <div>
      <h3 class="mb-3">To-Do List Insight</h3>
  
      <div v-if="loading" class="text-muted">Loading...</div>
  
      <div v-else>
        <!-- Task Table -->
        <table v-if="logs.length > 0" class="table table-bordered table-hover align-middle">
          <thead class="table-primary">
            <tr>
              <th>Task</th>
              <th>Status</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(log, idx) in logs" :key="idx" :class="getRowClass(log)">
              <td>{{ log.task }}</td>
              <td>
                <span v-html="getStatusIcon(log)"></span>
                {{ getStatusText(log) }}
              </td>
              <td>{{ formatDateTime(log.datetime) }}</td>
            </tr>
          </tbody>
        </table>
  
        <p v-else class="text-muted">No tasks found for this date.</p>
  
        <!-- Weekly Graphs in a Card -->
        <div v-if="weeklySummary.length > 0" class="mt-5">
          <div class="card shadow-sm p-4">
            <div class="row">
              <!-- Bar Chart -->
              <div class="col-md-8 d-flex justify-content-center align-items-center">
                <BarChart 
                  :chart-data="chartData" 
                  :chart-options="chartOptions"
                  :width= "900" :height= "450"
                />
              </div>
  
              <!-- Pie Chart -->
              <div class="col-md-4 d-flex justify-content-center align-items-center">
                <PieChart 
                  :chart-data="pieData" 
                  :chart-options="pieOptions"
                  style="width: 100%; max-width: 300px; height: 300px;" 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { ref, watch } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
} from 'chart.js'
import { Bar, Pie } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

const props = defineProps({
  selectedChildId: Number,
  selectedDate: String
})

const logs = ref([])
const weeklySummary = ref([])
const loading = ref(false)
const chartLoading = ref(false)
const accessToken = localStorage.getItem('access_token')

// Chart state
const chartData = ref({ labels: [], datasets: [] })
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Weekly To-Do Progress' }
  },
  scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
}
const pieData = ref({ labels: [], datasets: [] })
const pieOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    title: { display: true, text: 'Completion Ratio' }
  }
}

const BarChart = Bar
const PieChart = Pie

// ---- Fetch Daily Logs ----
const fetchDailyLogs = async () => {
  if (!props.selectedChildId || !props.selectedDate) return
  loading.value = true
  try {
    const res = await fetch(
      `http://localhost:5000/parent/child/${props.selectedChildId}/todo-logs?date=${props.selectedDate}`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    const data = await res.json()
    logs.value = data.logs || []
  } catch (err) {
    console.error('Failed to fetch To-Do daily logs:', err)
  } finally {
    loading.value = false
  }
}

// ---- Fetch Weekly Summary ----
const fetchWeeklySummary = async () => {
  if (!props.selectedChildId) return
  chartLoading.value = true
  try {
    const res = await fetch(
      `http://localhost:5000/parent/child/${props.selectedChildId}/todo-logs?week=true`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    const data = await res.json()
    weeklySummary.value = data.weekly_summary || []

    // Bar Chart Data
    chartData.value = {
      labels: weeklySummary.value.map((d) => d.date),
      datasets: [
        {
          label: 'Tasks Assigned',
          data: weeklySummary.value.map((d) => d.total_tasks),
          backgroundColor: '#0d6efd'
        },
        {
          label: 'Tasks Completed',
          data: weeklySummary.value.map((d) => d.completed_tasks),
          backgroundColor: '#28a745'
        }
      ]
    }

    // Pie Chart Data (Completion Ratio)
    const totalTasks = weeklySummary.value.reduce((sum, d) => sum + d.total_tasks, 0)
    const completedTasks = weeklySummary.value.reduce((sum, d) => sum + d.completed_tasks, 0)
    const pendingTasks = totalTasks - completedTasks

    pieData.value = {
      labels: ['Completed', 'Pending'],
      datasets: [
        {
          data: [completedTasks, pendingTasks],
          backgroundColor: ['#28a745', '#ffc107'],
          hoverBackgroundColor: ['#218838', '#e0a800']
        }
      ]
    }
  } catch (err) {
    console.error('Failed to fetch weekly summary:', err)
  } finally {
    chartLoading.value = false
  }
}

// Watch props
watch(() => props.selectedChildId, () => {
  fetchWeeklySummary()
  fetchDailyLogs()
}, { immediate: true })

watch(() => props.selectedDate, fetchDailyLogs)

// Helpers
const formatDateTime = (dt) => {
  const d = new Date(dt)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const isTodayTask = (log) => {
  const today = new Date().toISOString().split('T')[0]
  const taskDate = new Date(log.datetime).toISOString().split('T')[0]
  return taskDate === today && new Date(log.datetime) > new Date()
}

const isPastTask = (log) => {
  const today = new Date().toISOString().split('T')[0]
  const taskDate = new Date(log.datetime).toISOString().split('T')[0]
  return taskDate < today || (taskDate === today && new Date(log.datetime) <= new Date())
}

const getStatusText = (log) => {
  if (isPastTask(log)) return log.is_done ? 'Done' : 'Not Completed'
  if (isTodayTask(log)) return log.is_done ? 'Done' : 'Pending'
  return 'Upcoming'
}

const getStatusIcon = (log) => {
  if (isPastTask(log)) {
    return log.is_done
      ? `<i class="bi bi-check-circle-fill text-success"></i>`
      : `<i class="bi bi-x-circle-fill text-danger"></i>`
  }
  if (isTodayTask(log)) {
    return log.is_done
      ? `<i class="bi bi-check-circle-fill text-success"></i>`
      : `<i class="bi bi-hourglass-split text-warning"></i>`
  }
  return `<i class="bi bi-circle text-secondary"></i>`
}

const getRowClass = (log) => {
  const status = getStatusText(log)
  if (status === 'Done') return 'table-success'
  if (status === 'Not Completed') return 'table-danger'
  if (status === 'Pending') return 'table-warning'
  return 'table-secondary'
}
</script>



<style scoped>
.table td i {
  margin-right: 6px;
}



.card {
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.card .row {
  align-items: center;
}

.chart-container canvas {
  border-radius: 12px;
  background: #fdfdfd;
}

/* Overall page */
h3 {
  font-weight: 600;
  color: #0d6efd;
  margin-bottom: 20px;
}

/* Table Styling */
.table {
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
}

.table th {
  background: linear-gradient(135deg, #0d6efd, #0b5ed7);
  color: #fff;
  text-align: center;
  font-weight: 500;
  font-size: 15px;
  vertical-align: middle;
}

.table td {
  vertical-align: middle;
  text-align: center;
  font-size: 14px;
  color: #333;
  padding: 12px 10px;
  transition: background 0.2s ease;
}

.table-hover tbody tr:hover {
  background: rgba(13, 110, 253, 0.05);
}

/* Row status highlights */
.table-success {
  background: rgba(40, 167, 69, 0.1) !important;
}

.table-danger {
  background: rgba(220, 53, 69, 0.1) !important;
}

.table-warning {
  background: rgba(255, 193, 7, 0.1) !important;
}

.table-secondary {
  background: rgba(108, 117, 125, 0.1) !important;
}

/* Status Icons */
.table td i {
  margin-right: 8px;
  font-size: 16px;
  vertical-align: middle;
}

/* Card Styling */
.card {
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.12);
}

.card .row {
  align-items: stretch;
}

.card .col-md-8,
.card .col-md-4 {
  padding: 10px;
}

/* Chart Containers */
.chart-container canvas,
.card canvas {
  border-radius: 12px;
  background: #f9f9f9;
  padding: 10px;
}

/* Empty State Text */
.text-muted {
  font-style: italic;
  font-size: 14px;
}

/* Responsive Tweaks */
@media (max-width: 768px) {
  .card {
    padding: 20px 15px;
  }

  .table th,
  .table td {
    font-size: 13px;
    padding: 8px;
  }

  h3 {
    font-size: 20px;
  }
}

</style>
