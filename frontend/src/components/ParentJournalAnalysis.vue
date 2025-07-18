<template>
  <div class="parent-journal-analysis-bg">
    <main class="main-content">
      <div class="analysis-container">
        <!-- Filter Row + View All Entries -->
        <div class="filters-container" v-if="selectedChild && moodData.labels.length">
          <div class="filters-row">
            <label for="child">Select Child:</label>
            <select id="child" v-model="selectedChild">
              <option v-for="child in children" :key="child.id" :value="child.id">
                {{ child.name }}
              </option>
            </select>

            <label for="date">Select Date:</label>
            <input type="date" id="date" v-model="selectedDate" :max="today" />
          </div>

          <div class="entry-button-wrapper">
            <button class="view-btn" @click="showEntries = true">View All Entries</button>
          </div>
        </div>


        <!-- Heading -->
        <!-- <h2 v-if="selectedChild">
          {{ getChildName(selectedChild) }}'s Journal Activity
        </h2> -->

        <!-- Mood Graphs Row -->
        <div class="mood-graphs-row" v-if="moodData.labels.length">
          <div class="chart-card">
            <h3>Mood Fluctuation (Day)</h3>
            <line-chart :chart-data="moodData" :chart-options="moodOptions" style="height: 250px;" />
          </div>

          <div class="chart-card">
            <h3>Mood Distribution</h3>
            <pie-chart :chart-data="moodPieData" :chart-options="moodPieOptions" style="height: 250px;" />
          </div>
        </div>

        <!-- Weekly Chart -->
        <!-- Weekly Journal Count -->
        <div class="weekly-graph" v-if="weeklyData.labels.length">
          <div class="chart-card weekly-chart-card">
            <h3>Journals Written in Last 7 Days</h3>
            <div class="chart-wrapper">
              <bar-chart :chart-data="weeklyData" :chart-options="weeklyOptions" style="height: 350px;" />
            </div>
          </div>
        </div>


        <!-- No data -->
        <p v-if="!moodData.labels.length" class="no-data-msg">No journal data available for this date.</p>

        <!-- Modal -->
        <div class="modal-overlay" v-if="showEntries" @click.self="showEntries = false">
          <div class="modal-content">
            <h3>Journal Entries on {{ selectedDate }}</h3>
            <ul>
              <li v-for="entry in journalTexts" :key="entry.id">
                <strong>{{ formatTime(entry.timestamp) }}:</strong> {{ entry.content || '(No content)' }}
              </li>
            </ul>
            <button @click="showEntries = false" class="close-btn">✕ Close</button>
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
  LineElement, BarElement, ArcElement,
  PointElement, CategoryScale, LinearScale
} from 'chart.js'
import { Line, Bar, Pie } from 'vue-chartjs'

ChartJS.register(
  Title, Tooltip, Legend,
  LineElement, BarElement, ArcElement,
  PointElement, CategoryScale, LinearScale
)

export default {
  name: 'ParentJournalAnalysis',
  components: {
    lineChart: Line,
    barChart: Bar,
    pieChart: Pie
  },
  data() {
    const todayStr = new Date().toISOString().split('T')[0]
    return {
      children: [],
      selectedChild: null,
      selectedDate: todayStr,
      today: todayStr,

      moodData: { labels: [], datasets: [] },
      moodPieData: { labels: [], datasets: [] },
      weeklyData: { labels: [], datasets: [] },
      journalTexts: [],
      showEntries: false,

      moodOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            min: 1,
            max: 5,
            ticks: {
              stepSize: 1,
              callback: val => ['Sad', '', 'Neutral', '', 'Happy'][val - 1] || val
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              boxWidth: 10,
              font: { size: 10 }
            }
          }
        },
        layout: {
          padding: 0
        }
      },

      moodPieOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: { size: 10 },
              boxWidth: 10
            }
          },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.label}: ${ctx.parsed}%`
            }
          }
        }
      },

      weeklyOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          }
        },
        layout: {
          padding: 0
        }
      }

    }
  },
  watch: {
    selectedChild() {
      this.fetchWeeklyStats()
      this.fetchMoodByDate()
    },
    selectedDate() {
      this.fetchMoodByDate()
    }
  },
  mounted() {
    this.fetchChildren()
  },
  methods: {
    async fetchChildren() {
      try {
        const res = await fetch('http://localhost:5000/parent/children', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        })
        const data = await res.json()
        this.children = data.children || []
        if (this.children.length) {
          this.selectedChild = this.children[0].id
        }
      } catch (err) {
        console.error('Error fetching children:', err.message)
      }
    },

    async fetchMoodByDate() {
      try {
        const res = await fetch(
          `http://localhost:5000/parent/child/${this.selectedChild}/journal-by-date?date=${this.selectedDate}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        )
        const data = await res.json()
        const entries = data.journal_entries || []

        if (!entries.length) {
          this.resetMoodCharts()
          return
        }

        this.journalTexts = entries.map(e => ({
          id: e.id,
          timestamp: e.timestamp,
          content: e.content
        }))

        const moodLabels = entries.map(e =>
          new Date(e.timestamp).toLocaleTimeString('en-IN', {
            hour: '2-digit', minute: '2-digit'
          })
        )
        const moodScores = entries.map(e => this.mapMoodToScore(e.mood))
        const moodCounts = {}
        entries.forEach(e => {
          const mood = e.mood.toLowerCase()
          moodCounts[mood] = (moodCounts[mood] || 0) + 1
        })

        const pieLabels = Object.keys(moodCounts)
        const pieData = Object.values(moodCounts)
        const total = pieData.reduce((a, b) => a + b, 0)
        const piePercent = pieData.map(count => ((count / total) * 100).toFixed(1))

        this.moodData = {
          labels: moodLabels,
          datasets: [{
            label: 'Mood Score (1=Sad, 5=Happy)',
            data: moodScores,
            borderColor: '#ff6a88',
            backgroundColor: 'rgba(255,106,136,0.2)',
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: '#ff6a88'
          }]
        }

        this.moodPieData = {
          labels: pieLabels.map(m => m.charAt(0).toUpperCase() + m.slice(1)),
          datasets: [{
            label: 'Mood Distribution',
            data: piePercent,
            backgroundColor: ['#ff6a88', '#ffc371', '#8ae9c1', '#a9a0f3', '#ffb347']
          }]
        }
      } catch (err) {
        console.error('Error fetching mood by date:', err.message)
        this.resetMoodCharts()
      }
    },

    async fetchWeeklyStats() {
      try {
        const res = await fetch(
          `http://localhost:5000/parent/child/${this.selectedChild}/journal-entries?days=7`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        )
        const data = await res.json()
        const entries = data.journal_entries || []

        const dayMap = {}
        entries.forEach(e => {
          const day = new Date(e.date).toLocaleDateString('en-IN', { weekday: 'short' })
          dayMap[day] = (dayMap[day] || 0) + 1
        })

        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        const counts = days.map(day => dayMap[day] || 0)

        this.weeklyData = {
          labels: days,
          datasets: [{
            label: 'Journals Written',
            data: counts,
            backgroundColor: '#a4cafe',
            borderRadius: 8
          }]
        }
      } catch (err) {
        console.error('Error fetching weekly stats:', err.message)
      }
    },

    resetMoodCharts() {
      this.moodData = { labels: [], datasets: [] }
      this.moodPieData = { labels: [], datasets: [] }
      this.journalTexts = []
    },

    mapMoodToScore(mood) {
      const map = { sad: 1, angry: 2, neutral: 3, excited: 4, happy: 5 }
      return map[mood?.toLowerCase()] || 3
    },

    getChildName(id) {
      const child = this.children.find(c => c.id === id)
      return child ? child.name : ''
    },

    formatTime(ts) {
      return new Date(ts).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.parent-journal-analysis-bg {
  font-family: 'Comic Neue', cursive;
  background-color: #fff;
  /* min-height: 100vh; */
  /* padding: 2rem 0; */
}

.main-content {
  display: flex;
  justify-content: center;
  /* padding: 1rem; */
}

.analysis-container {
  background: white;
  /* padding: 30px; */
  border-radius: 20px;
  max-width: 1000px;
  width: 100%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.filters-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.filters-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  font-size: 14px;
}

.filters-row select,
.filters-row input {
  padding: 6px 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.entry-button-wrapper {
  margin-left: auto;
}


/* HEADER */
h2 {
  font-size: 1rem;
  color: #222;
  text-align: center;
  margin-bottom: 1.4rem;
  font-family: 'Fredoka One', cursive;
}

/* BUTTON */
.view-btn {
  background: #ff6a88;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  height: 36px;
  font-size: 14px;
  font-weight: bold;
}

/* CHARTS */
.mood-graphs-row {
  display: flex;
  gap: 24px;
  margin-top: 1rem;
  flex-wrap: wrap;
  justify-content: space-between;
}

.chart-card {
  background: #ffe6ec;
  padding: 18px;
  border-radius: 16px;
  flex: 1 1 45%;
  min-width: 300px;
  box-shadow: 0 4px 12px rgba(255, 106, 136, 0.08);
}

.chart-card h3 {
  color: #ff6a88;
  font-family: 'Fredoka One', cursive;
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.weekly-graph {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  width: 100%;
}

.weekly-chart-card {
  /* max-width: 600px; */
  width: 100%;
  background: #ffe6ec;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 106, 136, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.weekly-chart-card h3 {
  font-family: 'Fredoka One', cursive;
  color: #ff6a88;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
}

.chart-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}


/* MODAL */
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
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  font-size: 15px;
  line-height: 1.5;
}

.close-btn {
  margin-top: 1rem;
  background: #ccc;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.no-data-msg {
  text-align: center;
  margin-top: 2rem;
  color: #777;
  font-style: italic;
  font-size: 15px;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .mood-graphs-row {
    flex-direction: column;
    align-items: center;
  }

  .chart-card {
    width: 100%;
    min-width: unset;
  }

  .filters-container {
    flex-direction: column;
    align-items: flex-start;
  }

  .view-btn {
    width: 100%;
    margin-top: 0.5rem;
  }
}
</style>
