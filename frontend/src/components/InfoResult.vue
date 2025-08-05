<template>
  <div class="result-page">
    <!-- Back Button -->
    <button class="back-btn" @click="goBack">
      ← Back to Infotainment
    </button>

    <h1 class="result-title">
      <span v-if="topicTitle">News on "{{ topicTitle }}"</span>
      <span v-else-if="searchQuery">Search Results for "{{ searchQuery }}"</span>
    </h1>

    <div v-if="loading" class="loading">Loading news...</div>

    <!-- Articles -->
    <div 
      v-else-if="articles.length > 0" 
      :class="showMarkButton ? 'articles-list' : 'articles-grid'"
    >
      <div v-for="(article, index) in articles" :key="index" class="news-card">
        <div v-if="article.date" class="news-meta">
          <strong>{{ new Date(article.date).toLocaleDateString() }}</strong>
        </div>
        <h3 class="news-title">{{ article.title || 'Untitled' }}</h3>
        <p class="news-summary">{{ article.summary || article.content }}</p>
        <a v-if="article.read_more" :href="article.read_more" target="_blank" class="read-more">
          Read More →
        </a>
      </div>
    </div>

    <div v-else class="error">No news available.</div>

    <!-- Single Mark as Read Button -->
    <div v-if="showMarkButton" class="mark-btn-wrapper">
      <button
        class="mark-btn"
        :disabled="markLoading || markCompleted"
        @click="markAsRead"
      >
        <span v-if="markCompleted">Completed!</span>
        <span v-else-if="markLoading">Marking...</span>
        <span v-else>Mark as Read</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const topicTitle = ref(route.query.topic || "");
const searchQuery = ref(route.query.search || "");
const articles = ref([]);
const loading = ref(true);
const showMarkButton = ref(false);
const logId = ref(null);
const markCompleted = ref(false);
const markLoading = ref(false);

function goBack() {
  router.push({ name: "ChildInfotainment" });
}

async function markAsRead() {
  if (!logId.value) return;
  markLoading.value = true;
  try {
    const token = localStorage.getItem("access_token");
    const res = await fetch(`http://localhost:5000/infotainment/mark-read/${logId.value}`, {
      method: "PUT",
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    if (res.ok) {
      markCompleted.value = true;
      alert("Marked as read successfully!");
    } else {
      alert(data.error || "Could not mark as read.");
    }
  } catch (err) {
    console.error("Error marking as read:", err);
    alert("Something went wrong.");
  } finally {
    markLoading.value = false;
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem("access_token");

    if (topicTitle.value) {
      // Predefined topic (new content)
      const res = await fetch(`http://localhost:5000/infotainment/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ prompt: topicTitle.value })
      });
      const data = await res.json();
      if (res.ok && data.content) {
        const parsed = JSON.parse(data.content);
        articles.value = parsed;
        logId.value = data.log_id;
        showMarkButton.value = true; // Only show button for new generated content
      }
    } else if (searchQuery.value) {
      // Past news search
      const res = await fetch(
        `http://localhost:5000/infotainment/search?q=${encodeURIComponent(searchQuery.value)}`,
        { headers: { "Authorization": `Bearer ${token}` } }
      );
      const data = await res.json();
      if (res.ok && data.logs) {
        let parsedArticles = [];
        data.logs.forEach((log) => {
          try {
            const parsed = JSON.parse(log.content);
            if (Array.isArray(parsed)) {
              parsed.forEach((item) => parsedArticles.push({ ...item, date: log.date }));
            } else {
              parsedArticles.push({ title: "Past News", summary: log.content, date: log.date });
            }
          } catch {
            parsedArticles.push({ title: "Past News", summary: log.content, date: log.date });
          }
        });
        articles.value = parsedArticles;
        showMarkButton.value = false; // No mark button for past search results
      }
    }
  } catch (err) {
    console.error("Error fetching news:", err);
    articles.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.result-page {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.5rem;
  font-family: 'Poppins', sans-serif;
}

.back-btn {
  display: inline-block;
  margin-bottom: 1.5rem;
  padding: 10px 18px;
  background-color: #3498db;
  color: white;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
.back-btn:hover { background-color: #2980b9; }

.result-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.articles-list { /* single column for new content */
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.news-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.news-meta { font-size: 0.85rem; color: #666; margin-bottom: 0.5rem; }
.news-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem; color: #34495e; }
.news-summary { font-size: 0.95rem; line-height: 1.6; color: #2c3e50; margin-bottom: 1rem; }
.read-more { font-weight: 600; color: #3498db; text-decoration: none; }

.mark-btn-wrapper { text-align: center; margin-top: 2rem; }
.mark-btn {
  padding: 12px 20px;
  background-color: #9b59b6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.mark-btn:disabled {
  background-color: #c7a4d6;
  cursor: not-allowed;
}
</style>
