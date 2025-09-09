<template>
  <div class="parent-journal-analysis-bg">
    <main class="main-content">
      <div class="analysis-container">
        <p v-if="!moodData.labels.length" class="no-data-msg">No journal data available for this date.</p>
        <p v-if="!weeklyData.labels.length && moodData.labels.length" class="no-data-msg">No journal data available for the last 7 days.</p>

        <div v-if="moodData.labels.length" class="entry-button-wrapper">
          <button class="view-btn" @click="showEntries = true">View Journal Entries</button>
        </div>

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

        <div class="weekly-graph" v-if="weeklyData.labels.length">
          <div class="chart-card weekly-chart-card">
            <h3>Journals Written in Last 7 Days</h3>
            <div class="chart-wrapper">
              <bar-chart :chart-data="weeklyData" :chart-options="weeklyOptions" style="height: 350px;" />
            </div>
          </div>
        </div>

        <div class="modal-overlay" v-if="showEntries" @click.self="showEntries = false">
          <div class="modal-content">
            <h3>Journal Entries on {{ selectedDate }}</h3>
            <ul>
              <li v-for="entry in journalTexts" :key="entry.id">
                <div class="entry-header">
                  <strong>{{ entry.timestamp }}</strong>
                  <span class="mood-display">{{ entry.mood }}</span>
                </div>
                <p class="entry-content">{{ entry.content || '(No content written)' }}</p>
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
    lineChart: Line,
    barChart: Bar,
    pieChart: Pie
  },
  data() {
    return {
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
              callback: val => ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'][val - 1] || val
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
        layout: { padding: 0 }
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
              label: ctx => `${ctx.label}: ${ctx.parsed}%`
            }
          }
        }
      },
      weeklyOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          }
        },
        layout: { padding: 0 }
      }
    }
  },
  watch: {
    selectedChildId: {
      handler() {
        this.fetchWeeklyStats()
        this.fetchMoodByDate()
      },
      immediate: true
    },
    selectedDate() {
      this.fetchMoodByDate()
    }
  },
  methods: {
    formatTime(timeStr) {
      if (!timeStr) return '';
      const [hourStr, minuteStr] = timeStr.split(':');
      const hour = parseInt(hourStr, 10);
      const ampm = hour >= 12 ? 'PM' : 'AM';
      const hour12 = hour % 12 || 12;
      return `${hour12.toString().padStart(2, '0')}:${minuteStr} ${ampm}`;
    },
    async fetchMoodByDate() {
      try {
        const res = await fetch(
          `https://slice-abcd.onrender.com/parent/child/${this.selectedChildId}/journal-by-date?date=${this.selectedDate}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        )
        const data = await res.json()
        const entries = data.journal_entries || []

        if (!entries.length) {
          this.resetMoodCharts()
          return
        }
        
        // Populate journalTexts with timestamp, mood, AND content
        this.journalTexts = entries.map(e => ({
          id: e.id,
          timestamp: this.formatTime(e.timestamp),
          mood: e.mood ? e.mood.charAt(0).toUpperCase() + e.mood.slice(1) : 'Unknown',
          content: e.content
        }));

        const moodLabels = entries.map(e => this.formatTime(e.timestamp));

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
            label: 'Mood Score (1=Very Negative, 5=Very Positive)',
            data: moodScores,
            borderColor: '#5A4FCF',
            backgroundColor: 'rgba(90, 79, 207, 0.2)',
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: '#5A4FCF'
          }]
        }

        this.moodPieData = {
          labels: pieLabels.map(m => m.charAt(0).toUpperCase() + m.slice(1)),
          datasets: [{
            label: 'Mood Distribution',
            data: piePercent,
            backgroundColor: ['#5A4FCF', '#ffc371', '#8ae9c1', '#a9a0f3', '#ffb347', '#ff6b6b', '#48dbfb', '#feca57', '#1dd1a1', '#ff9f43']
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
          `https://slice-abcd.onrender.com/parent/child/${this.selectedChildId}/journal-entries?days=7`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
        )
        const data = await res.json()
        const entries = data.journal_entries || []

        const dayMap = {}
        const today = new Date();
        const labels = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(today.getDate() - i);
            const day = date.toLocaleDateString('en-IN', { weekday: 'short' });
            labels.push(day);
            dayMap[day] = 0;
        }

        entries.forEach(e => {
          const day = new Date(e.date).toLocaleDateString('en-IN', { weekday: 'short' })
          if(dayMap.hasOwnProperty(day)) {
            dayMap[day] += 1
          }
        })

        const counts = labels.map(day => dayMap[day]);

        this.weeklyData = {
          labels: labels,
          datasets: [{
            label: 'Journals Written',
            data: counts,
            backgroundColor: '#5A4FCF', 
            borderRadius: 8
          }]
        }
      } catch (err) {
        console.error('Error fetching weekly stats:', err.message)
        this.weeklyData = { labels: [], datasets: [] }
      }
    },
    resetMoodCharts() {
      this.moodData = { labels: [], datasets: [] }
      this.moodPieData = { labels: [], datasets: [] }
      this.journalTexts = []
    },
    mapMoodToScore(mood) {
      const moodStr = mood?.toLowerCase() || 'neutral';
      const scoreMap = {
        'happy': 5, 'joyful': 5, 'grateful': 5, 'proud': 5, 'excited': 5,
        'hopeful': 4, 'relaxed': 4,
        'neutral': 3, 'nostalgic': 3, 'apathetic': 3,
        'sad': 2, 'lonely': 2, 'bored': 2, 'tired': 2, 'disappointed': 2, 'embarrassed': 2, 'sarcastic': 2,
        'angry': 1, 'depressed': 1, 'anxious': 1, 'frustrated': 1, 'scared': 1, 'worried': 1, 'upset': 1, 'stressed': 1
      };
      return scoreMap[moodStr] || 3;
    },
  }
}
</script>

<style scoped>
.parent-journal-analysis-bg {
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
  max-width: 1000px;
  width: 100%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.entry-button-wrapper {
  text-align: right;
  margin-bottom: 1rem;
}
.view-btn {
  background: #5A4FCF;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 50px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: transform 0.3s, background-color 0.3s;
}
.view-btn:hover {
  transform: scale(1.05);
  background-color: #F7D96F;
  color: #4A4A4A;
}
.mood-graphs-row {
  display: flex;
  gap: 24px;
  margin-top: 1rem;
  flex-wrap: wrap;
  justify-content: space-between;
}
.chart-card {
  background: #E6E6FA;
  padding: 18px;
  border-radius: 16px;
  flex: 1 1 45%;
  min-width: 300px;
  box-shadow: 0 4px 12px rgba(90, 79, 207, 0.08);
}
.chart-card h3 {
  color: #5A4FCF;
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
  width: 100%;
  background: #E6E6FA;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(90, 79, 207, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.weekly-chart-card h3 {
  font-family: 'Fredoka One', cursive;
  color: #5A4FCF;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
}
.chart-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}
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
  line-height: 1.6;
}
.modal-content h3 {
    color: #5A4FCF;
    font-family: 'Fredoka One', cursive;
    margin-top: 0;
    margin-bottom: 1.5rem;
    text-align: center;
}
.modal-content ul {
    list-style-type: none;
    padding: 0;
}
.modal-content li {
    padding: 12px 5px;
    border-bottom: 1px solid #eee;
}
.modal-content li:last-child {
    border-bottom: none;
}
.entry-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 1.1em;
}
.mood-display {
    background-color: #E6E6FA;
    color: #5A4FCF;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.9em;
    font-weight: bold;
}
.entry-content {
    margin: 0;
    color: #333;
    padding-left: 5px;
}
.close-btn {
  display: block;
  margin: 1.5rem auto 0;
  background: #ccc;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.close-btn:hover {
    background: #bbb;
}
.no-data-msg {
  text-align: center;
  margin-top: 2rem;
  margin-bottom: 2rem;
  color: #777;
  font-style: italic;
  font-size: 15px;
}
@media (max-width: 768px) {
  .mood-graphs-row {
    flex-direction: column;
    align-items: center;
  }
  .chart-card {
    width: 100%;
    min-width: unset;
  }
}
</style>