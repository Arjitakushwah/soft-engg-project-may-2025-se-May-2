<template>
  <header class="custom-navbar">
    <div class="left-section">
      <h2>Hi, <span class="highlight">{{ greetingName }}</span></h2>
    </div>
    <div class="right-section">
      <button @click="goToDashboard" class="logout-button">
        {{ dashboardLabel }}
      </button>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// reactive values
const role = ref('')
const userName = ref('User')
const greetingName = ref('User')
const dashboardLabel = ref('Dashboard')

onMounted(() => {
  // Simulate localStorage data (for frontend-only mode)
  if (!localStorage.getItem('role')) {
    // You can switch these values to test
    localStorage.setItem('role', 'Child')      //  'child'
    localStorage.setItem('name', 'child') 
    //localStorage.setItem('role', 'parent')      //  'parent'
    //localStorage.setItem('name', 'Parent')      
  }

  role.value = localStorage.getItem('role')
  userName.value = localStorage.getItem('name') || 'User'

  // set greeting and label
  greetingName.value = role.value === 'parent' ? 'Parent' : userName.value
  dashboardLabel.value = role.value === 'parent' ? 'Parent Dashboard' : 'Child Dashboard'
})

const goToDashboard = () => {
  if (role.value === 'parent') {
    localStorage.clear()
    router.push('/parent_dashboard')
  } else {
    localStorage.clear()
    router.push('/child_dashboard')
  }
}

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.custom-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1d1d2e;
  padding: 20px 30px;
  color: white;
}

.left-section h2 {
  margin: 0;
  font-size: 24px;
}

.left-section .highlight {
  color: #00f8ff;
}

.right-section .logout-button {
  background-color: #ff4d5a;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #e03a46;
}
</style>
