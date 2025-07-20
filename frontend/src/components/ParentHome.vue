<template>
  <div class="parent-home-container">
    <h2 class="title">Welcome, {{ parentName }}</h2>
    <p class="subtitle">Use the sidebar to manage your child’s learning activities.</p>

    <div class="child-cards">
      <h3 class="section-title">Your Children</h3>
      <div class="card-grid">
        <div v-for="child in children" :key="child.id" class="child-card">
          <h4>{{ child.name }}</h4>
          <p><strong>Age:</strong> {{ child.age }}</p>
          <p><strong>Gender:</strong> {{ child.gender }}</p>
          <button class="btn btn-primary btn-sm mt-2" @click="fetchChildProfile(child.id)">
            View Profile
          </button>
        </div>
      </div>
      <p v-if="!children.length" class="no-child-msg">No children added yet.</p>
    </div>

    <!-- Modal -->
    <transition name="modal-fade">
  <div v-if="showModal" class="modal-backdrop">
    <div class="modal-content">
      <span class="modal-close" @click="showModal = false">×</span>

      <h4 class="modal-title">{{ profile.name }}'s Profile</h4>
      <p><strong>Age:</strong> {{ profile.age }}</p>
      <p><strong>Gender:</strong> {{ profile.gender }}</p>
      <p><strong>Streak:</strong> {{ profile.streak }}</p>
      <p><strong>Longest Streak:</strong> {{ profile.longest_streak }}</p>
      <p><strong>Badges:</strong> {{ profile.badges }}</p>

      <button class="btn btn-success mt-3" @click="downloadChildReport(profile.id)">
        Download Weekly Report
      </button>
    </div>
  </div>
</transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const parentName = ref('Parent')
const children = ref([])
const showModal = ref(false)
const profile = ref({})

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  const res = await fetch('http://localhost:5000/parent/children', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const data = await res.json()
  if (res.ok) {
    children.value = data.children
  }
  
  const parent = JSON.parse(localStorage.getItem('parent'))
  if (parent?.name) parentName.value = parent.name
})

const fetchChildProfile = async (childId) => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(`http://localhost:5000/parent/child/${childId}/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await res.json()
    if (res.ok) {
      profile.value = data.profile
      showModal.value = true
    } else {
      alert(data.error || 'Failed to fetch profile')
    }
  } catch (err) {
    alert('Network error')
  }
}

const downloadChildReport = async (childId) => {
  const token = localStorage.getItem('access_token');
  const summaryRange = 'weekly'; // Change to 'monthly' if needed

  try {
    const url = `http://localhost:5000/parent/child-analysis?child_id=${childId}&summary_range=${summaryRange}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Error: ${response.status} - ${errText}`);
    }

    const blob = await response.blob();
    const fileUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = fileUrl;
    a.download = `child_analysis_report_${childId}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(fileUrl);
  } catch (error) {
    console.error('Download error:', error);
    alert(error.message || 'Error downloading report');
  }
};





</script>

<style scoped>
.parent-home-container {
  font-family: 'Comic Neue', cursive;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.title {
  font-size: 2.2rem;
  color: #ff6a88;
  margin-bottom: 1rem;
  font-family: 'Fredoka One', cursive;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 2rem;
}

.child-list {
  text-align: left;
  margin-top: 30px;
  max-width: 500px;
  margin-inline: auto;
}

.child-item {
  padding: 10px;
  background-color: #fef3f7;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 1rem;
  color: #444;
}


.child-cards {
  text-align: left;
  margin-top: 2rem;
}

.section-title {
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.child-card {
  background-color: #fef3f7;
  padding: 1.2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  text-align: center;
}

.child-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.child-card h4 {
  color: #ff6a88;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.child-card p {
  margin: 0.3rem 0;
  font-size: 0.95rem;
  color: #555;
}

.no-child-msg {
  color: #999;
  font-style: italic;
  text-align: center;
  margin-top: 1rem;
}

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  position: relative;
  background: #fff;
  padding: 2rem;
  border-radius: 14px;
  width: 90%;
  max-width: 400px;
  text-align: left;
  font-family: 'Comic Neue', cursive;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  animation: pop-in 0.3s ease;
}

.modal-title {
  font-size: 1.4rem;
  color: #ff6a88;
  margin-bottom: 1rem;
}

/* Animations */
@keyframes pop-in {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.btn-success {
  background-color: #28a745;
  border: none;
  color: white;
  padding: 8px 16px;
  font-size: 0.95rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-success:hover {
  background-color: #218838;
}

.modal-close {
  position: absolute;
  top: 1px;
  right: 16px;
  font-size: 2.5rem;
  color: #888;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.2s ease;
}

.modal-close:hover {
  color: #ff6a88;
}

</style>
