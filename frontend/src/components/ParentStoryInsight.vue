<template>
    <div class="parent-infotainment-analysis-bg">
      <main class="main-content">
        <div class="analysis-container">
  
          <!-- Daily Logs Table -->
          <div v-if="storyLogs.length === 0" class="text-muted">No logs available for {{ selectedDate }}.</div>
          <table v-else class="table table-bordered table-striped align-middle text-center">
            <thead class="table-dark">
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
                    {{ log.is_done ? 'Completed' : 'Not Done' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
  
          <!-- Weekly Chart -->
          <div v-if="storyChart.labels.length" class="graph-wrapper">
            <div class="chart-card">
              <h3>Story Sessions (Last 7 Days)</h3>
              <bar-chart
                :chart-data="storyChart"
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
              backgroundColor: '#ffb6b9',
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
    padding: 10px;
    border-radius: 20px;
    width: 100%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  }
  
  .chart-card {
    background: #ffe7e7;
    padding: 20px;
    border-radius: 16px;
    margin-top: 1rem;
    box-shadow: 0 4px 12px rgba(255, 182, 185, 0.25);
  }
  
  .chart-card h3 {
    color: #e91e63;
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
  
  .text-muted {
    text-align: center;
    color: #777;
    font-style: italic;
    font-size: 15px;
    margin-top: 2rem;
  }
  </style>
  