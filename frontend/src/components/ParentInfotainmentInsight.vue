<template>
  <div class="parent-infotainment-analysis-bg">
    <main class="main-content">
      <div class="analysis-container">

        <div class="card shadow-sm p-4 mb-4">
          <h4 class="card-title">Daily Infotainment Logs</h4>
          <div v-if="infotainmentLogs.length === 0" class="text-center text-muted no-data-text">
            No logs available for {{ selectedDate }}.
          </div>
          <table v-else class="table table-bordered table-hover align-middle text-center">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Prompt</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in infotainmentLogs" :key="log.id">
                <td>{{ selectedDate }}</td>
                <td>{{ formatTime(log.time) }}</td>
                <td>{{ log.child_prompt }}</td>
                <td>
                  <span v-html="getStatusIcon(log)"></span>&nbsp;
                  <span :class="getStatusTextColorClass(log)">
                    {{ log.is_done ? 'Completed' : 'Not Read' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="infotainmentData.labels.length" class="graph-wrapper">
          <div class="chart-card weekly-chart-card">
            <h4 class="chart-title">Infotainment Sessions (Last 7 Days)</h4>
            <div class="chart-wrapper">
              <bar-chart
                :chart-data="infotainmentData"
                :chart-options="chartOptions"
                style="height: 350px;"
              />
            </div>
          </div>
        </div>
        <p v-else class="text-center text-muted no-data-text">No weekly data available for the last 7 days.</p>
      </div>
    </main>
  </div>
</template>


<script>
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
)

export default {
  name: 'ParentInfotainmentInsight',
  props: {
    selectedChildId: {
      type: [String, Number],
      required: true
    },
    selectedDate: {
      type: String,
      required: true
    }
  },
  components: {
    barChart: Bar
  },
  data() {
    return {
      infotainmentData: { labels: [], datasets: [] },
      infotainmentLogs: [],
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { display: false },
            title: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    }
  },
  watch: {
    selectedChildId: {
      handler() {
        this.fetchInfotainmentStats();
      },
      immediate: true
    },
    selectedDate: {
      handler() {
        this.fetchInfotainmentStats();
      },
      immediate: true
    }
  },
  methods: {
    formatTime(timeStr) {
      if (!timeStr) return '';
      const [hourStr, minuteStr] = timeStr.split(':');
      const hour = parseInt(hourStr, 10);
      const minute = parseInt(minuteStr, 10);
      const ampm = hour >= 12 ? 'PM' : 'AM';
      const hour12 = hour % 12 || 12;
      return `${hour12.toString().padStart(2, '0')}:${minuteStr} ${ampm}`;
    },
    async fetchInfotainmentStats() {
      try {
        // Weekly chart data
        const weeklyRes = await fetch(
          `http://localhost:5000/parent/child/${this.selectedChildId}/infotainment-logs?week=true`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        );
        const weeklyData = await weeklyRes.json();
        const summary = weeklyData.weekly_summary || [];
        const countMap = {};
        summary.forEach(entry => {
          countMap[entry.date] = entry.topics_read;
        });

        const start = new Date(weeklyData.week_start);
        const end = new Date(weeklyData.week_end);
        const labels = [], values = [];

        while (start <= end) {
          const dateStr = start.toISOString().split('T')[0];
          const dayLabel = start.toLocaleDateString('en-IN', { weekday: 'short' });
          labels.push(dayLabel);
          values.push(countMap[dateStr] || 0);
          start.setDate(start.getDate() + 1);
        }

        this.infotainmentData = {
          labels,
          datasets: [{
            label: 'Topics Read',
            data: values,
            backgroundColor: '#5A4FCF',
            borderRadius: 8
          }]
        };

        // Daily logs data
        const dailyRes = await fetch(
          `http://localhost:5000/parent/child/${this.selectedChildId}/infotainment-logs?date=${this.selectedDate}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        );
        const dailyData = await dailyRes.json();
        this.infotainmentLogs = dailyData.logs || [];

      } catch (err) {
        console.error('Error fetching infotainment stats:', err.message);
        this.infotainmentData = { labels: [], datasets: [] };
        this.infotainmentLogs = [];
      }
    },
    getStatusIcon(log) {
      return log.is_done
        ? `<i class="fas fa-check-circle text-success"></i>`
        : `<i class="fas fa-exclamation-circle text-warning"></i>`;
    },
    getStatusTextColorClass(log) {
        return log.is_done ? 'status-text-done' : 'status-text-not-done';
    }
  }
}

</script>
<style scoped>
.parent-infotainment-analysis-bg {
  font-family: 'Comic Neue', cursive;
  background-color: #fff;
  min-height: 100vh;
}

.main-content {
  display: flex;
  justify-content: center;
}

.analysis-container {
  background: white;
  padding: 30px;
  border-radius: 20px;
  width: 100%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* Card Styling */
.card {
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-bottom: 2rem;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.12);
}

.card-title {
  font-family: 'Fredoka One', cursive;
  color: #5A4FCF;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

/* Table Styling */
.table {
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
}


.table tbody tr {
  background-color: white;
}


.table thead th {
  background-color: #4FCFDE;
  color: #333;
  text-align: center;
  font-weight: 500;
  font-size: 15px;
  vertical-align: middle;
}

/* Table cell borders */
.table th,
.table td {
  border: 0.25px solid #f5f5f5;
}

/* Table data cells styling */
.table td {
  vertical-align: middle;
  text-align: center;
  font-size: 14px;
  color: #333;
  padding: 12px 10px;
  transition: background 0.2s ease;
}

/* Status Text Colors and Icons */
.table td i {
    margin-right: 6px;
}

.status-text-done { color: #28a745; font-weight: bold; }
.status-text-not-done { color: #ffc107; font-weight: bold; }

/* Chart Styling */
.chart-card {
  background: #E6E6FA;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 106, 136, 0.08);
  width: 100%;
  display: flex;
  flex-direction: column;
}

.chart-title {
  color: #5A4FCF;
  text-align: center;
  font-family: 'Fredoka One', cursive;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.graph-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.chart-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.no-data-text {
  text-align: center;
  color: #777;
  font-style: italic;
  font-size: 1rem;
  margin-top: 2rem;
}

/* Responsive */
@media (max-width: 768px) {
  .analysis-container {
    padding: 15px;
  }
}
</style>