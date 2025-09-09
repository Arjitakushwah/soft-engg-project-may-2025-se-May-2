<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center gap-3">
        <button
          class="btn d-md-none"
          @click="$emit('toggle-sidebar')"
          aria-label="Toggle sidebar"
        >
          <i class="bi bi-list fs-3"></i>
        </button>
        <router-link to="/" class="navbar-brand app-title">
          Skill Explorers
        </router-link>
      </div>

      <div class="navbar-links">
        <template v-if="userRole === 'parent'">
          <button @click="goToDashboard" class="nav-btn-secondary">Dashboard</button>
          <button @click="navigateToPage('ParentEditProfile')" class="nav-btn-secondary">Edit Profile</button>
          <button @click="logout" class="nav-btn-primary">Logout</button>
        </template>
        <template v-else-if="userRole === 'child'">
          <button @click="goToDashboard" class="nav-btn-secondary">My Dashboard</button>
          <button @click="navigateToPage('ChildEditProfile')" class="nav-btn-secondary">Edit Profile</button>
          <button @click="logout" class="nav-btn-primary">Logout</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const emit = defineEmits(['navigate', 'logout', 'toggle-sidebar'])

const userRole = ref('')
const username = ref('')

onMounted(() => {
  userRole.value = localStorage.getItem('userRole')
  username.value = localStorage.getItem('username') || ''
})

const goToDashboard = () => {
  const role = localStorage.getItem('userRole')
  if (role === 'child') {
    router.push({ path: '/child/home' })
  } else if (role === 'parent') {
    router.push({ path: '/Parent/home' })
  }
}

const logout = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (token) {
      const response = await fetch('https://slice-abcd.onrender.com/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Logout failed on the server.');
      }
    }
  } catch (error) {
    console.error('Logout failed:', error);
  } finally {
    localStorage.clear()
    router.push({ path: '/' })
  }
}

const navigateToPage = (page) => {
  console.log('Navigating to:', page)
  router.push({ name: page })
}
</script>

<style scoped>

.navbar {
  background-color: #E6E6FA !important;
}

.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: #4e41df !important;
  text-decoration: none;
}

.welcome-text {
  font-family: 'Comic Neue', cursive;
  font-size: 2rem;
  font-weight: bold;
  color: #4e41df;
}

.btn-outline-primary {
  background-color: white;
  border-color: #3b82f6;
  color: #ff6a88;
  border: none;
  margin-left: 10px;
  padding: 10px 20px;
  font-family: 'Fredoka One', cursive;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.btn-outline-primary:hover {
  transform: scale(1.05);
  background-color: #faf2f4;
}

.btn-outline-success {
  background: white;
  border-color: #4e41df;
  color: #4e41df;
}

.btn-outline-success:hover {
  background-color: #4e41df;
  color: white;
}

.btn-danger {
  background-color: #ef4444;
  border-color: #ef4444;
}

.btn-danger:hover {
  background-color: #dc2626;
  border-color: #dc2626;
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-btn-secondary, .nav-btn-primary {
  font-family: 'Fredoka One', cursive;
  font-size: 1.1rem;
  padding: 10px 24px;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  text-decoration: none;
}

.nav-btn-secondary {
  background: transparent;
  border: 2px solid #5A4FCF;
  color: #5A4FCF;
}

.nav-btn-secondary:hover {
  background-color: #5A4FCF;
  color: white;
  transform: translateY(-2px);
}

.nav-btn-primary {
  background-color: #5A4FCF;
  color: white;
  border: 2px solid #5A4FCF;
}

.nav-btn-primary:hover {
  background-color: #F7D96F;
  border-color: #F7D96F;
  color: #4A4A4A;
  transform: translateY(-2px);
}

.navbar-link {
  display: none; 
}
</style>
