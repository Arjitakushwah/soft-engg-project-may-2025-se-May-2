<template>
  <div class="parent-infotainment-analysis-bg">
    <main class="main-content">
      <div class="analysis-container">
        <div class="card shadow-sm p-4 mb-4">
          <h4 class="card-title">Daily Story Logs</h4>
          <div v-if="storyLogs.length === 0" class="text-center text-muted no-data-text">
            No logs available for {{ selectedDate }}.
          </div>
          <table v-else class="table table-bordered align-middle text-center">
            <thead class="table-primary">
              <tr>
                <th>Date</th>
                <th>Theme</th>
                <th>Story Title</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in storyLogs" :key="log.id">
                <td>{{ selectedDate }}</td>
                <td>{{ log.theme }}</td>
                <td>{{ log.title }}</td>
                <td>
                  <span :class="log.is_done ? 'text-success' : 'text-warning'">
                    <i :class="log.is_done ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                    {{ log.is_done ? 'Completed' : 'Not Done' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="storyChart.labels.length" class="graph-wrapper">
          <div class="chart-card weekly-chart-card">
            <h4 class="chart-title">Story Sessions (Last 7 Days)</h4>
            <div class="chart-wrapper">
              <bar-chart
                :chart-data="storyChart"
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
  name: 'ParentStoryInsight',
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
      storyChart: { labels: [], datasets: [] },
      storyLogs: [],
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
        this.fetchStoryStats();
      },
      immediate: true
    },
    selectedDate: {
      handler() {
        this.fetchStoryStats();
      },
      immediate: true
    }
  },
  methods: {
    async fetchStoryStats() {
      try {
        // Fetch weekly chart data
        const weeklyRes = await fetch(
          `http://localhost:5000/parent/child/${this.selectedChildId}/story-logs?week=true`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        );
        const weeklyData = await weeklyRes.json();
        const summary = weeklyData.weekly_summary || [];

        const countMap = {};
        summary.forEach(entry => {
          countMap[entry.date] = entry.stories_read;
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

        this.storyChart = {
          labels,
          datasets: [{
            label: 'Stories Read',
            data: values,
            backgroundColor: '#5A4FCF', // Changed to purple to match the theme
            borderRadius: 8
          }]
        };

        // Fetch daily story logs
        const dailyRes = await fetch(
          `http://localhost:5000/parent/child/${this.selectedChildId}/story-logs?date=${this.selectedDate}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        );
        const dailyData = await dailyRes.json();
        this.storyLogs = dailyData.logs || [];

      } catch (err) {
        console.error('Error fetching story stats:', err.message);
        this.storyChart = { labels: [], datasets: [] };
        this.storyLogs = [];
      }
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

/* New card styling for the table */
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

.table {
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
}

/* Updated table header and striped rows */
.table th {
  background: #4FCFDE; /* Light blue color from your image */
  color: #333;
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

.table tbody tr:nth-of-type(odd) {
  background-color: white;
}

.table tbody tr:nth-of-type(even) {
  background-color: #F7D96F; /* Light yellow color from your image */
}

/* Updated status text with bold font-weight */
.table .text-success,
.table .text-warning {
  font-weight: bold;
}

.table-success { color: #28a745; }
.table-warning { color: #ffc107; }

/* Chart Styling */
.chart-card {
  background: #E6E6FA;
  padding: 20px;
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