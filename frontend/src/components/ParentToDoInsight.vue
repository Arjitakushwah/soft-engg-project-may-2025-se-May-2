<template>
  <div class="to-do-insight-container">
    <div v-if="loading" class="text-center text-muted">Loading...</div>

    <div v-else>
      <div class="card shadow-sm p-4 mb-5">
        <h4 class="card-title">Daily Task Log</h4>
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
                <span v-html="getStatusIcon(log)"></span>&nbsp;
                <span :class="getStatusTextColorClass(log)">
                  {{ getStatusText(log) }}
                </span>
              </td>
              <td>{{ formatDateTime(log.datetime) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="text-center text-muted no-data-text">No tasks found for this date.</p>
      </div>

      <div v-if="weeklySummary.length > 0" class="graphs-container">
        <div class="chart-card weekly-chart-card">
          <h4 class="chart-title">Weekly To-Do Progress</h4>
          <BarChart :chart-data="chartData" :chart-options="chartOptions" style="height: 350px" />
        </div>

        <div class="chart-card pie-chart-card">
          <h4 class="chart-title">Completion Ratio (7 Days)</h4>
          <PieChart :chart-data="pieData" :chart-options="pieOptions" style="height: 300px" />
        </div>
      </div>
      <p v-else-if="!chartLoading" class="text-center text-muted no-data-text">No weekly summary data available.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'vue-chartjs';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

const props = defineProps({
  selectedChildId: Number,
  selectedDate: String,
});

const logs = ref([]);
const weeklySummary = ref([]);
const loading = ref(false);
const chartLoading = ref(false);
const accessToken = localStorage.getItem('access_token');

// Chart state
const chartData = ref({ labels: [], datasets: [] });
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { boxWidth: 10, font: { size: 10 } },
    },
    title: { display: false },
  },
  scales: {
    y: { beginAtZero: true, ticks: { stepSize: 1 } },
    x: { grid: { display: false } },
  },
};

const pieData = ref({ labels: [], datasets: [] });
const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { font: { size: 10 }, boxWidth: 10 },
    },
    title: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => `${ctx.label}: ${ctx.parsed}%`,
      },
    },
  },
};

const BarChart = Bar;
const PieChart = Pie;

// ---- Fetch Daily Logs ----
const fetchDailyLogs = async () => {
  if (!props.selectedChildId || !props.selectedDate) return;
  loading.value = true;
  try {
    const res = await fetch(
      `http://localhost:5000/parent/child/${props.selectedChildId}/todo-logs?date=${props.selectedDate}`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );
    const data = await res.json();
    logs.value = data.logs || [];
  } catch (err) {
    console.error('Failed to fetch To-Do daily logs:', err);
  } finally {
    loading.value = false;
  }
};

// ---- Fetch Weekly Summary ----
const fetchWeeklySummary = async () => {
  if (!props.selectedChildId) return;
  chartLoading.value = true;
  try {
    const res = await fetch(
      `http://localhost:5000/parent/child/${props.selectedChildId}/todo-logs?week=true`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );
    const data = await res.json();
    weeklySummary.value = data.weekly_summary || [];

    // Bar Chart Data
    chartData.value = {
      labels: weeklySummary.value.map((d) => d.date),
      datasets: [
        {
          label: 'Tasks Assigned',
          data: weeklySummary.value.map((d) => d.total_tasks),
          backgroundColor: '#5A4FCF', // Matches your brand's blue
          borderRadius: 8,
        },
        {
          label: 'Tasks Completed',
          data: weeklySummary.value.map((d) => d.completed_tasks),
          backgroundColor: '#F7D96F', // Matches your brand's yellow
          borderRadius: 8,
        },
      ],
    };

    // Pie Chart Data (Completion Ratio)
    const totalTasks = weeklySummary.value.reduce((sum, d) => sum + d.total_tasks, 0);
    const completedTasks = weeklySummary.value.reduce((sum, d) => sum + d.completed_tasks, 0);
    const pendingTasks = totalTasks - completedTasks;

    pieData.value = {
      labels: ['Completed', 'Pending'],
      datasets: [
        {
          data: [completedTasks, pendingTasks],
          backgroundColor: ['#5A4FCF', '#ffc107'],
          hoverOffset: 8,
        },
      ],
    };
  } catch (err) {
    console.error('Failed to fetch weekly summary:', err);
  } finally {
    chartLoading.value = false;
  }
};

// Watch props
watch(
  () => props.selectedChildId,
  () => {
    fetchWeeklySummary();
    fetchDailyLogs();
  },
  { immediate: true }
);

watch(() => props.selectedDate, fetchDailyLogs);

// Helpers
const formatDateTime = (dt) => {
  const d = new Date(dt);
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const isTodayTask = (log) => {
  const today = new Date().toISOString().split('T')[0];
  const taskDate = new Date(log.datetime).toISOString().split('T')[0];
  return taskDate === today && new Date(log.datetime) > new Date();
};

const isPastTask = (log) => {
  const today = new Date().toISOString().split('T')[0];
  const taskDate = new Date(log.datetime).toISOString().split('T')[0];
  return taskDate < today || (taskDate === today && new Date(log.datetime) <= new Date());
};

const getStatusText = (log) => {
  if (isPastTask(log)) return log.is_done ? 'Done' : 'Not Done';
  if (isTodayTask(log)) return log.is_done ? 'Done' : 'Pending';
  return 'Upcoming';
};

const getStatusIcon = (log) => {
  if (isPastTask(log)) {
    return log.is_done
      ? `<i class="fas fa-check-circle text-success"></i>`
      : `<i class="fas fa-exclamation-circle text-warning"></i>`;
  }
  if (isTodayTask(log)) {
    return log.is_done
      ? `<i class="fas fa-check-circle text-success"></i>`
      : `<i class="fas fa-hourglass-half text-warning"></i>`;
  }
  return `<i class="fas fa-circle text-secondary"></i>`;
};

const getRowClass = (log) => {
  const status = getStatusText(log);
  if (status === 'Done') return 'table-success-bg';
  if (status === 'Not Done') return 'table-danger-bg';
  if (status === 'Pending') return 'table-warning-bg';
  return '';
};

const getStatusTextColorClass = (log) => {
  const status = getStatusText(log);
  if (status === 'Done') return 'status-text-done';
  if (status === 'Not Done') return 'status-text-not-done';
  return 'status-text-pending';
}
</script>

<style scoped>


.to-do-insight-container {
  font-family: 'Comic Neue', cursive;
}

.page-title {
  font-family: 'Fredoka One', cursive;
  color: #5A4FCF;
  font-size: 1.8rem;
  font-weight: bold;
}

.card-title {
  font-family: 'Fredoka One', cursive;
  color: #5A4FCF;
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.graphs-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-top: 2rem;
}

.chart-card {
  background: #E6E6FA;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 106, 136, 0.08);
  display: flex;
  flex-direction: column;
}

.weekly-chart-card {
  flex: 2;
}

.pie-chart-card {
  flex: 1;
}

.no-data-text {
  text-align: center;
  font-style: italic;
  font-size: 1rem;
  margin: 2rem 0;
}


.table {
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  width: 100%;
}


.table th {
  background: #4FCFDE; 
  color: #333;
  text-align: center;
  font-weight: 500;
  font-size: 15px;
  vertical-align: middle;
}

.table tbody tr {
  background-color: white; /* All rows have white background */
}

/* Row status highlights */
.table-success-bg { background-color: rgba(40, 167, 69, 0.1) !important; }
.table-danger-bg { background-color: rgba(220, 53, 69, 0.1) !important; }
.table-warning-bg { background-color: rgba(255, 193, 7, 0.1) !important; }

/* Status Text Colors and Bolding */
.status-text-done { color: #28a745; font-weight: bold; }
.status-text-not-done { color: #F7D96F; font-weight: bold; }
.status-text-pending { color: #ffc107; font-weight: bold; }

.table-hover tbody tr:hover {
  background: rgba(13, 110, 253, 0.05);
}

.table td i {
  margin-right: 6px;
}

/* Chart.js styles */
.chart-card h4.chart-title {
  color: #5A4FCF;
  font-family: 'Fredoka One', cursive;
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 992px) {
  .graphs-container {
    grid-template-columns: 1fr;
  }
}
</style>