<template>
  <div class="parent-home-container">
    <h2 class="title">Welcome, {{ parentName }}</h2>
    <p class="subtitle">Use the sidebar to manage your child’s learning activities.</p>

    <div class="child-list mt-5">
      <h3>Your Children</h3>
      <ul v-if="children.length">
        <li v-for="child in children" :key="child.id" class="child-item">
          👶 {{ child.name }} ({{ child.age }} yrs, {{ child.gender }})
          <button class="btn btn-sm btn-outline-info ms-2" @click="fetchChildProfile(child.id)">View Profile</button>
        </li>
      </ul>
      <p v-else>No children added yet.</p>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <h4>{{ profile.name }}'s Profile</h4>
        <p><strong>Age:</strong> {{ profile.age }}</p>
        <p><strong>Gender:</strong> {{ profile.gender }}</p>
        <p><strong>Streak:</strong> {{ profile.streak }}</p>
        <p><strong>Longest Streak:</strong> {{ profile.longest_streak }}</p>
        <p><strong>Badges:</strong> {{ profile.badges }}</p>
        <button class="btn btn-secondary mt-3" @click="showModal = false">Close</button>
      </div>
    </div>
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

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  width: 350px;
  text-align: left;
  font-family: 'Comic Neue', cursive;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
</style>
