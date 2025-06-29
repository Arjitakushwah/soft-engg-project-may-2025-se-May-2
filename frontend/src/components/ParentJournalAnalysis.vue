<template>
  <div class="parent-journal-analysis-bg">
    <main class="main-content">
      <div class="analysis-container">
        <div class="child-select">
          <label for="child">Select Child:</label>
          <select id="child" v-model="selectedChild">
            <option v-for="child in children" :key="child" :value="child">{{ child }}</option>
          </select>
        </div>
        <h2>{{ selectedChild }}</h2>
        <div class="charts-grid">
          <div class="chart-card">
            <h3>Mood Over Last 7 Days</h3>
            <line-chart :chart-data="moodData" :chart-options="moodOptions" />
          </div>
          <div class="chart-card">
            <h3>Word Count Per Day</h3>
            <bar-chart :chart-data="wordCountData" :chart-options="wordCountOptions" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

import { Line, Bar } from 'vue-chartjs'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale
)

export default {
  name: 'ParentJournalAnalysis',
  components: {
    lineChart: Line,
    barChart: Bar
  },
  data() {
    return {
      children: ['Anya', 'Ravi', 'Meera'],
      selectedChild: 'Anya',

      moodData: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
          {
            label: 'Mood Score (1=Sad, 5=Happy)',
            data: [3, 4, 2, 5, 4, 3, 5],
            borderColor: '#ff6a88',
            backgroundColor: 'rgba(255,106,136,0.2)',
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: '#ff6a88'
          }
        ]
      },
      moodOptions: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: false }
        },
        scales: {
          y: {
            min: 1,
            max: 5,
            ticks: {
              stepSize: 1,
              callback: value => ['Sad', '', 'Neutral', '', 'Happy'][value - 1] || value
            }
          }
        }
      },
      wordCountData: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
          {
            label: 'Word Count',
            data: [120, 200, 150, 180, 220, 170, 210],
            backgroundColor: '#ff6a88',
            borderRadius: 8
          }
        ]
      },
      wordCountOptions: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.parent-journal-analysis-bg {
  font-family: 'Comic Neue', cursive;
  /* background: linear-gradient(to bottom right, #f0f8ff, #ffe6f0); */
  /* min-height: 100vh; */
  color: #333;
  display: flex;
  flex-direction: column;
}

.main-content {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  /* padding: 2rem; */
  /* min-height: calc(100vh - 100px); */
}

.analysis-container {
  background: white;
  padding: 30px 24px;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  /* max-width: 900px; */
  width: 100%;
  margin: 0 auto;
}

.analysis-container h2 {
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  font-size: 2.2rem;
  margin-bottom: 30px;
  text-align: center;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.chart-card {
  background: #ffe6ec;
  border-radius: 18px;
  box-shadow: 0 4px 12px rgba(255, 106, 136, 0.08);
  padding: 22px 18px 18px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-card h3 {
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  font-size: 1rem;
  margin-bottom: 18px;
  text-align: center;
}

.child-select {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  font-size: 16px;
}

.child-select select {
  padding: 6px 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}


@media (max-width: 900px) {
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
</style>