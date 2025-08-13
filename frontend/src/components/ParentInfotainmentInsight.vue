<template>
    <div class="parent-infotainment-analysis-bg">
      <main class="main-content">
        <div class="analysis-container">
  
          <!-- Table for today’s logs -->
          <div v-if="infotainmentLogs.length === 0" class="text-muted">No logs available for {{ selectedDate }}.</div>
          <table v-else class="table table-bordered table-striped align-middle text-center">
            <thead class="table-dark">
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
                  <span :class="log.is_done ? 'text-success' : 'text-warning'">
                    {{ log.is_done ? 'Completed' : 'Not Read' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
  
          <!-- Weekly Chart -->
          <div v-if="infotainmentData.labels.length" class="graph-wrapper">
            <div class="chart-card">
              <h3>Infotainment Sessions (Last 7 Days)</h3>
              <bar-chart
                :chart-data="infotainmentData"
                :chart-options="chartOptions"
                style="height: 300px;"
              />
            </div>
          </div>
  
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
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
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
            backgroundColor: '#ffc371',
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
    }
  },
  mounted() {
    this.fetchInfotainmentStats();

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
    padding: 10px;
    border-radius: 20px;
    width: 100%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  }
  
  .chart-card {
    background: #fff4e0;
    padding: 20px;
    border-radius: 16px;
    margin-top: 1rem;
    box-shadow: 0 4px 12px rgba(255, 195, 113, 0.15);
  }
  
  .chart-card h3 {
    color: #ff9800;
    text-align: center;
    font-family: 'Fredoka One', cursive;
    margin-bottom: 1rem;
    font-size: 1rem;
  }
  
  .graph-wrapper {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .no-data-msg {
    text-align: center;
    color: #777;
    font-style: italic;
    font-size: 15px;
    margin-top: 2rem;
  }
  </style>
  